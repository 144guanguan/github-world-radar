#!/usr/bin/env python3
"""Build and validate deterministic Markdown artifacts from daily radar JSON."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence
from urllib.parse import parse_qsl, urlparse


STAGES = {
    "concept_experiment": "概念实验",
    "early_exploration": "早期探索",
    "rapid_growth": "快速成长",
    "stable_development": "稳定发展",
    "reviving_mature": "成熟项目重新升温",
}
CONFIDENCE = {"high": "高", "medium": "中", "low": "低"}
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9_.-]{0,99})/[A-Za-z0-9](?:[A-Za-z0-9_.-]{0,99})$")
RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$")
SENSITIVE_QUERY_KEYS = {
    "access_token",
    "auth",
    "authorization",
    "credential",
    "key",
    "password",
    "secret",
    "signature",
    "sig",
    "token",
    "x-amz-credential",
    "x-amz-signature",
}
GENERATED_ROOTS = ("docs/daily", "docs/projects", "docs/assets", "docs/indexes", "data/generated")
README_START = "<!-- RADAR:GENERATED:START -->"
README_END = "<!-- RADAR:GENERATED:END -->"
CATEGORIES = {
    "established_momentum": "明确势头",
    "overlooked_cross_domain": "跨领域潜力",
    "surprising_and_experimental": "意外发现",
}
CHANGE_TYPES = {
    "new": "新进入视野",
    "rising": "明显升温",
    "cooling": "热度下降",
    "major_progress": "重大进展",
    "exited": "退出观察",
    "previous_judgement_revised": "判断修正",
    "stable": "持续观察",
}


class RadarError(Exception):
    """Represent an actionable input, generation, or validation failure."""


@dataclass(frozen=True)
class Artifact:
    """Describe one generated repository-relative text artifact."""

    path: str
    content: str


def _is_text(value: Any) -> bool:
    """Return whether value is a non-empty string after trimming."""

    return isinstance(value, str) and bool(value.strip())


def _require_text(obj: Mapping[str, Any], key: str, where: str) -> str:
    """Read a required non-empty string and report its logical location."""

    value = obj.get(key)
    if not _is_text(value):
        raise RadarError(f"{where}.{key} must be a non-empty string")
    return value.strip()


def _parse_date(value: str, where: str) -> date:
    """Parse an ISO calendar date or raise a contextual validation error."""

    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise RadarError(f"{where} must be an ISO date (YYYY-MM-DD)") from exc


def _parse_timestamp(value: str, where: str) -> datetime:
    """Parse an ISO timestamp and require an explicit timezone offset."""

    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise RadarError(f"{where} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise RadarError(f"{where} must include a timezone offset")
    return parsed


def _validate_url(value: str, where: str, *, github_repo: str | None = None) -> str:
    """Validate a public HTTP(S) URL and reject embedded credentials or secrets."""

    if any(char.isspace() for char in value):
        raise RadarError(f"{where} contains whitespace")
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise RadarError(f"{where} must be an absolute HTTP(S) URL")
    if parsed.username or parsed.password:
        raise RadarError(f"{where} must not embed credentials")
    query_keys = {key.lower() for key, _ in parse_qsl(parsed.query, keep_blank_values=True)}
    if query_keys & SENSITIVE_QUERY_KEYS:
        raise RadarError(f"{where} contains a sensitive query parameter")
    if github_repo is not None:
        expected = f"github.com/{github_repo.lower()}"
        actual = f"{parsed.netloc.lower()}{parsed.path.rstrip('/').lower()}"
        if parsed.scheme != "https" or actual != expected:
            raise RadarError(f"{where} must equal https://github.com/{github_repo}")
    return value


def _validate_source(source: Any, where: str) -> dict[str, str]:
    """Validate and normalize one evidence source entry."""

    if not isinstance(source, dict):
        raise RadarError(f"{where} must be an object")
    label_value = source.get("label", source.get("type"))
    if not _is_text(label_value):
        raise RadarError(f"{where}.type or {where}.label must be a non-empty string")
    label = label_value.strip()
    url = _validate_url(_require_text(source, "url", where), f"{where}.url")
    checked_value = source.get("checked_at", source.get("observed_at"))
    if not _is_text(checked_value):
        raise RadarError(f"{where}.observed_at or {where}.checked_at must be a timestamp")
    checked_at = checked_value.strip()
    _parse_timestamp(checked_at, f"{where}.checked_at")
    return {"label": label, "url": url, "checked_at": checked_at}


def _validate_project(project: Any, where: str) -> dict[str, Any]:
    """Validate and normalize one project observation."""

    if not isinstance(project, dict):
        raise RadarError(f"{where} must be an object")
    repository_value = project.get("repository", project.get("full_name"))
    if not _is_text(repository_value):
        raise RadarError(f"{where}.full_name or {where}.repository is required")
    repository = repository_value.strip()
    if not REPOSITORY_RE.fullmatch(repository):
        raise RadarError(f"{where}.repository must use owner/repo with safe characters")
    if "repository" in project and "full_name" in project:
        if str(project["repository"]).lower() != str(project["full_name"]).lower():
            raise RadarError(f"{where}.repository and {where}.full_name must identify the same repository")
    repo_id_value = project.get("repo_id", repository.lower())
    if isinstance(repo_id_value, int) and not isinstance(repo_id_value, bool) and repo_id_value >= 0:
        normalized_repo_id = str(repo_id_value)
    elif _is_text(repo_id_value):
        normalized_repo_id = repo_id_value.strip()
    else:
        raise RadarError(f"{where}.repo_id must be a non-empty stable identifier")
    description_value = project.get("description", project.get("summary"))
    if not _is_text(description_value):
        raise RadarError(f"{where}.summary or {where}.description is required")
    signal_value = project.get("what_it_signals", project.get("signal"))
    if not _is_text(signal_value):
        raise RadarError(f"{where}.what_it_signals or {where}.signal is required")
    category = project.get("category")
    change_type = project.get("change_type")
    if category is None and change_type is None:
        category = "established_momentum"
        change_type = "stable"
    if category is None:
        category = "surprising_and_experimental" if change_type == "new" else "established_momentum"
    if change_type is None:
        change_type = "stable"
    if category not in CATEGORIES:
        raise RadarError(f"{where}.category must be one of {sorted(CATEGORIES)}")
    if change_type not in CHANGE_TYPES:
        raise RadarError(f"{where}.change_type must be one of {sorted(CHANGE_TYPES)}")
    tags = project.get("tags", [])
    if not isinstance(tags, list) or not all(_is_text(tag) for tag in tags):
        raise RadarError(f"{where}.tags must be an array of non-empty strings")
    normalized_tags = [tag.strip() for tag in tags]
    if len(normalized_tags) != len(set(normalized_tags)):
        raise RadarError(f"{where}.tags contains duplicates")
    risks = project.get("risks", [])
    if not isinstance(risks, list) or not all(_is_text(risk) for risk in risks):
        raise RadarError(f"{where}.risks must be an array of non-empty strings")
    metrics = project.get("metrics", {})
    if not isinstance(metrics, dict):
        raise RadarError(f"{where}.metrics must be an object")
    momentum = project.get("momentum", {})
    if not isinstance(momentum, dict):
        raise RadarError(f"{where}.momentum must be an object")
    normalized: dict[str, Any] = {
        "repo_id": normalized_repo_id,
        "repository": repository,
        "url": _validate_url(
            _require_text(project, "url", where), f"{where}.url", github_repo=repository
        ),
        "domain": _require_text(project, "domain", where),
        "description": description_value.strip(),
        "why_now": _require_text(project, "why_now", where),
        "signal": signal_value.strip(),
        "stage": _require_text(project, "stage", where),
        "confidence": _require_text(project, "confidence", where),
        "tags": normalized_tags,
        "category": category,
        "change_type": change_type,
        "risks": [risk.strip() for risk in risks],
        "recommended_action": str(project.get("recommended_action", "持续跟踪")).strip(),
    }
    if not normalized["recommended_action"]:
        raise RadarError(f"{where}.recommended_action must be a non-empty string")
    if normalized["stage"] not in STAGES:
        raise RadarError(f"{where}.stage must be one of {sorted(STAGES)}")
    if normalized["confidence"] not in CONFIDENCE:
        raise RadarError(f"{where}.confidence must be one of {sorted(CONFIDENCE)}")
    for integer_key in ("stars", "forks"):
        value = metrics.get(integer_key, project.get(integer_key))
        if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value < 0):
            raise RadarError(f"{where}.{integer_key} must be a non-negative integer or null")
        normalized[integer_key] = value
    for integer_key in ("contributors",):
        value = metrics.get(integer_key)
        if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value < 0):
            raise RadarError(f"{where}.metrics.{integer_key} must be a non-negative integer or null")
        normalized[integer_key] = value
    last_activity = project.get("last_activity")
    latest_commit_at = metrics.get("latest_commit_at")
    latest_release_at = metrics.get("latest_release_at")
    for timestamp_key, value in (("latest_commit_at", latest_commit_at), ("latest_release_at", latest_release_at)):
        if value is not None:
            if not _is_text(value):
                raise RadarError(f"{where}.metrics.{timestamp_key} must be a timestamp or null")
            _parse_timestamp(value, f"{where}.metrics.{timestamp_key}")
        normalized[timestamp_key] = value
    if last_activity is None and latest_commit_at:
        last_activity = _parse_timestamp(latest_commit_at, f"{where}.metrics.latest_commit_at").date().isoformat()
    if last_activity is not None:
        if not _is_text(last_activity):
            raise RadarError(f"{where}.last_activity must be an ISO date or null")
        _parse_date(last_activity, f"{where}.last_activity")
        normalized["last_activity"] = last_activity
    else:
        normalized["last_activity"] = None
    license_name = metrics.get("license", project.get("license"))
    if license_name is not None and not _is_text(license_name):
        raise RadarError(f"{where}.license must be a string or null")
    normalized["license"] = license_name.strip() if isinstance(license_name, str) else None
    for momentum_key in ("stars_7d", "stars_30d"):
        value = momentum.get(momentum_key)
        if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value < 0):
            raise RadarError(f"{where}.momentum.{momentum_key} must be a non-negative integer or null")
        normalized[momentum_key] = value
    proxy_signals = momentum.get("proxy_signals", [])
    if not isinstance(proxy_signals, list) or not all(_is_text(item) for item in proxy_signals):
        raise RadarError(f"{where}.momentum.proxy_signals must be an array of strings")
    normalized["proxy_signals"] = [item.strip() for item in proxy_signals]
    sources = project.get("sources", project.get("evidence"))
    if not isinstance(sources, list) or not sources:
        raise RadarError(f"{where}.sources must be a non-empty array")
    normalized["sources"] = [
        _validate_source(source, f"{where}.sources[{index}]")
        for index, source in enumerate(sources)
    ]
    source_urls = [source["url"] for source in normalized["sources"]]
    if len(source_urls) != len(set(source_urls)):
        raise RadarError(f"{where}.sources contains duplicate URLs")
    image = project.get("image")
    if image is not None:
        if not isinstance(image, dict):
            raise RadarError(f"{where}.image must be an object or null")
        normalized["image"] = {
            "url": _validate_url(_require_text(image, "url", f"{where}.image"), f"{where}.image.url"),
            "alt": _require_text(image, "alt", f"{where}.image"),
            "license": _require_text(image, "license", f"{where}.image"),
        }
    return normalized


def validate_run(raw: Any, source_name: str = "run") -> dict[str, Any]:
    """Validate and normalize one complete daily run document."""

    if not isinstance(raw, dict):
        raise RadarError(f"{source_name} must contain a JSON object")
    if raw.get("schema_version") != 1:
        raise RadarError(f"{source_name}.schema_version must be 1")
    run_id = _require_text(raw, "run_id", source_name)
    if not RUN_ID_RE.fullmatch(run_id):
        raise RadarError(f"{source_name}.run_id contains unsafe characters")
    run_date = _require_text(raw, "date", source_name)
    parsed_date = _parse_date(run_date, f"{source_name}.date")
    generated_at = _require_text(raw, "generated_at", source_name)
    parsed_generated = _parse_timestamp(generated_at, f"{source_name}.generated_at")
    if parsed_generated.date() != parsed_date:
        raise RadarError(f"{source_name}.generated_at local date must match date")
    window = raw.get("window")
    if not isinstance(window, dict):
        raise RadarError(f"{source_name}.window must be an object")
    window_start = _require_text(window, "start", f"{source_name}.window")
    window_end = _require_text(window, "end", f"{source_name}.window")
    if _parse_date(window_start, f"{source_name}.window.start") > _parse_date(
        window_end, f"{source_name}.window.end"
    ):
        raise RadarError(f"{source_name}.window.start must not be after window.end")
    trends = raw.get("trends")
    if not isinstance(trends, list) or not trends or not all(_is_text(item) for item in trends):
        raise RadarError(f"{source_name}.trends must be a non-empty array of strings")
    normalized_trends = [item.strip() for item in trends]
    if len(normalized_trends) != len(set(normalized_trends)):
        raise RadarError(f"{source_name}.trends contains duplicates")
    projects = raw.get("projects")
    if not isinstance(projects, list) or not projects:
        raise RadarError(f"{source_name}.projects must be a non-empty array")
    normalized_projects = [
        _validate_project(project, f"{source_name}.projects[{index}]")
        for index, project in enumerate(projects)
    ]
    repositories = [project["repository"].lower() for project in normalized_projects]
    if len(repositories) != len(set(repositories)):
        raise RadarError(f"{source_name}.projects contains duplicate repositories")
    repo_ids = [project["repo_id"] for project in normalized_projects]
    if len(repo_ids) != len(set(repo_ids)):
        raise RadarError(f"{source_name}.projects contains duplicate repo_id values")
    return {
        "schema_version": 1,
        "run_id": run_id,
        "date": run_date,
        "generated_at": generated_at,
        "window": {"start": window_start, "end": window_end},
        "summary": _require_text(raw, "summary", source_name),
        "trends": normalized_trends,
        "projects": normalized_projects,
    }


def safe_path(repo: Path, relative: str) -> Path:
    """Resolve a repository-relative path and reject traversal or symlink escapes."""

    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise RadarError(f"unsafe repository-relative path: {relative}")
    root = repo.resolve()
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise RadarError(f"path escapes repository: {relative}") from exc
    return resolved


def load_runs(repo: Path) -> list[dict[str, Any]]:
    """Load all run JSON files in deterministic order and reject duplicate identities."""

    runs_dir = safe_path(repo, "data/runs")
    if not runs_dir.is_dir():
        raise RadarError("data/runs does not exist or is not a directory")
    files = sorted(runs_dir.glob("*.json"), key=lambda item: item.name)
    if not files:
        raise RadarError("data/runs contains no JSON run files")
    runs: list[dict[str, Any]] = []
    for path in files:
        if path.is_symlink() or not path.is_file():
            raise RadarError(f"run input must be a regular non-symlink file: {path.name}")
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise RadarError(f"cannot read valid JSON from data/runs/{path.name}: {exc}") from exc
        runs.append(validate_run(raw, f"data/runs/{path.name}"))
    run_ids = [run["run_id"] for run in runs]
    dates = [run["date"] for run in runs]
    if len(run_ids) != len(set(run_ids)):
        raise RadarError("data/runs contains duplicate run_id values")
    if len(dates) != len(set(dates)):
        raise RadarError("data/runs contains more than one run for the same date")
    identity_map: dict[str, str] = {}
    repository_map: dict[str, str] = {}
    for run in runs:
        for project in run["projects"]:
            repo_id = project["repo_id"]
            repository = project["repository"].lower()
            if repo_id in identity_map and identity_map[repo_id] != repository:
                raise RadarError(f"repo_id {repo_id!r} maps to multiple repositories")
            if repository in repository_map and repository_map[repository] != repo_id:
                raise RadarError(f"repository {repository!r} maps to multiple repo_id values")
            identity_map[repo_id] = repository
            repository_map[repository] = repo_id
    return sorted(runs, key=lambda run: (run["date"], run["run_id"]))


def _escape_markdown(value: str) -> str:
    """Escape table-breaking Markdown characters while preserving readable text."""

    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def _project_slug(repository: str) -> str:
    """Convert a validated owner/repo identifier to a stable filename stem."""

    if not REPOSITORY_RE.fullmatch(repository):
        raise RadarError(f"unsafe repository identifier: {repository}")
    return repository.replace("/", "--")


def _number(value: int | None) -> str:
    """Render an optional integer without inventing unavailable data."""

    return f"{value:,}" if value is not None else "数据不可得"


def _front_matter(title: str, description: str) -> str:
    """Create deterministic, safely quoted YAML front matter."""

    return "---\n" + f"title: {json.dumps(title, ensure_ascii=False)}\n" + f"description: {json.dumps(description, ensure_ascii=False)}\n" + "---\n\n"


def _render_daily(run: Mapping[str, Any]) -> str:
    """Render one evidence-backed daily report as Markdown."""

    lines = [
        _front_matter(f"GitHub 世界雷达 · {run['date']}", run["summary"]).rstrip(),
        f"# GitHub 世界雷达 · {run['date']}",
        "",
        f"> 生成时间：`{run['generated_at']}` · 观察窗口：`{run['window']['start']}` 至 `{run['window']['end']}` · Run：`{run['run_id']}`",
        "",
        run["summary"],
        "",
        "## 今日趋势",
        "",
    ]
    lines.extend(f"- {trend}" for trend in run["trends"])
    lines.extend(
        [
            "",
            "## 跨领域发现",
            "",
            "| 项目 | 领域 | 它是什么 | 为什么现在 | 信号 | 阶段 | 置信度 |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for project in run["projects"]:
        slug = _project_slug(project["repository"])
        lines.append(
            "| "
            + " | ".join(
                [
                    f"[{_escape_markdown(project['repository'])}](../projects/{slug}.md)",
                    _escape_markdown(project["domain"]),
                    _escape_markdown(project["description"]),
                    _escape_markdown(project["why_now"]),
                    _escape_markdown(project["signal"]),
                    STAGES[project["stage"]],
                    CONFIDENCE[project["confidence"]],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            f"![本期项目领域分布](../assets/trends-{run['date']}.svg)",
            "",
            f"![本期变化信号分布](../assets/signals-{run['date']}.svg)",
            "",
        ]
    )
    return "\n".join(lines)


def _render_project(repository: str, observations: Sequence[tuple[Mapping[str, Any], Mapping[str, Any]]]) -> str:
    """Render a project dossier from all chronological observations."""

    latest_run, latest = observations[-1]
    lines = [
        _front_matter(repository, latest["description"]).rstrip(),
        f"# [{repository}]({latest['url']})",
        "",
        latest["description"],
        "",
        "## 当前快照",
        "",
        f"- 领域：{latest['domain']}",
        f"- 阶段：{STAGES[latest['stage']]}",
        f"- 置信度：{CONFIDENCE[latest['confidence']]}",
        f"- Stars：{_number(latest['stars'])}",
        f"- Forks：{_number(latest['forks'])}",
        f"- 最近活动：{latest['last_activity'] or '数据不可得'}",
        f"- License：{latest['license'] or '未核验'}",
        f"- 稳定标识：`{latest['repo_id']}`",
        f"- 变化类型：{CHANGE_TYPES[latest['change_type']]}",
        f"- 发现类别：{CATEGORIES[latest['category']]}",
        f"- 7 日 Star 增量：{_number(latest['stars_7d'])}",
        f"- 30 日 Star 增量：{_number(latest['stars_30d'])}",
        f"- 推荐行动：{latest['recommended_action']}",
        f"- 最近收录：[日报 {latest_run['date']}](../daily/{latest_run['date']}.md)",
        "",
        "## 为什么值得关注",
        "",
        latest["why_now"],
        "",
        f"公开信号：{latest['signal']}",
        "",
    ]
    if latest.get("image"):
        image = latest["image"]
        lines.extend(
            [
                f"![{image['alt']}]({image['url']})",
                "",
                f"图片授权/使用条件：{image['license']}",
                "",
            ]
        )
    lines.extend(["## 证据", ""])
    for source in latest["sources"]:
        lines.append(f"- [{source['label']}]({source['url']})（核验于 `{source['checked_at']}`）")
    lines.extend(["", "## 观察历史", ""])
    for run, project in reversed(observations):
        lines.append(
            f"- [{run['date']}](../daily/{run['date']}.md)：{project['signal']}（{STAGES[project['stage']]}）"
        )
    lines.append("")
    if latest["tags"]:
        lines.extend(["## 标签", "", " · ".join(f"`{tag}`" for tag in latest["tags"]), ""])
    if latest["proxy_signals"]:
        lines.extend(["## 代理信号", ""])
        lines.extend(f"- {signal}" for signal in latest["proxy_signals"])
        lines.append("")
    if latest["risks"]:
        lines.extend(["## 风险与边界", ""])
        lines.extend(f"- {risk}" for risk in latest["risks"])
        lines.append("")
    return "\n".join(lines)


def _render_index(runs: Sequence[Mapping[str, Any]]) -> str:
    """Render the human-readable report index from all runs."""

    latest = runs[-1]
    lines = [
        _front_matter("GitHub 世界雷达", "跨领域、证据驱动的 GitHub 每日发现档案").rstrip(),
        "# GitHub 世界雷达",
        "",
        "这里持续记录 GitHub 上跨领域的新项目、升温信号与意外发现。",
        "",
        f"最新一期：[{latest['date']}](daily/{latest['date']}.md)",
        "",
        "## 日报归档",
        "",
    ]
    for run in reversed(runs):
        lines.append(
            f"- [{run['date']}](daily/{run['date']}.md) — {_escape_markdown(run['summary'])}（{len(run['projects'])} 个项目）"
        )
    lines.append("")
    return "\n".join(lines)


def _render_readme_fragment(runs: Sequence[Mapping[str, Any]]) -> str:
    """Render the complete generated README marker block."""

    latest = runs[-1]
    return "\n".join(
        [
            README_START,
            "## 最新雷达",
            "",
            f"- 最新日报：[{latest['date']}](docs/daily/{latest['date']}.md)",
            f"- 本期项目：{len(latest['projects'])} 个，覆盖 {len({p['domain'] for p in latest['projects']})} 个领域",
            "- [浏览完整索引](docs/index.md)",
            "",
            README_END,
            "",
        ]
    )


def _latest_observations(
    runs: Sequence[Mapping[str, Any]],
) -> list[tuple[Mapping[str, Any], Mapping[str, Any]]]:
    """Return each repository's most recent observation in stable repository order."""

    latest: dict[str, tuple[Mapping[str, Any], Mapping[str, Any]]] = {}
    for run in runs:
        for project in run["projects"]:
            latest[project["repo_id"]] = (run, project)
    return sorted(latest.values(), key=lambda item: item[1]["repository"].lower())


def _render_project_index(
    title: str,
    description: str,
    observations: Sequence[tuple[Mapping[str, Any], Mapping[str, Any]]],
) -> str:
    """Render a reusable project index table for a filtered set of observations."""

    lines = [
        _front_matter(title, description).rstrip(),
        f"# {title}",
        "",
        description,
        "",
        "| 项目 | 领域 | 变化 | 最近收录 |",
        "| --- | --- | --- | --- |",
    ]
    if observations:
        for run, project in observations:
            slug = _project_slug(project["repository"])
            lines.append(
                f"| [{_escape_markdown(project['repository'])}](../projects/{slug}.md) | "
                f"{_escape_markdown(project['domain'])} | {CHANGE_TYPES[project['change_type']]} | "
                f"[{run['date']}](../daily/{run['date']}.md) |"
            )
    else:
        lines.append("| 暂无符合条件的项目 | — | — | — |")
    lines.append("")
    return "\n".join(lines)


def _render_domain_index(
    observations: Sequence[tuple[Mapping[str, Any], Mapping[str, Any]]],
) -> str:
    """Render all current projects grouped by primary problem domain."""

    grouped: dict[str, list[tuple[Mapping[str, Any], Mapping[str, Any]]]] = defaultdict(list)
    for observation in observations:
        grouped[observation[1]["domain"]].append(observation)
    lines = [
        _front_matter("领域索引", "按问题领域浏览当前收录项目").rstrip(),
        "# 领域索引",
        "",
        "按项目所解决的问题领域归类；实现技术不替代问题领域。",
        "",
    ]
    for domain in sorted(grouped):
        lines.extend([f"## {domain}", ""])
        for run, project in grouped[domain]:
            slug = _project_slug(project["repository"])
            lines.append(
                f"- [{project['repository']}](../projects/{slug}.md) — {project['description']}（[{run['date']}](../daily/{run['date']}.md)）"
            )
        lines.append("")
    return "\n".join(lines)


def _render_svg(run: Mapping[str, Any]) -> str:
    """Render an accessible deterministic SVG bar chart for domain coverage."""

    counts = sorted(Counter(project["domain"] for project in run["projects"]).items(), key=lambda item: (-item[1], item[0]))
    width = 960
    row_height = 42
    top = 92
    height = top + row_height * len(counts) + 48
    label_width = 245
    max_bar = 610
    maximum = max(count for _, count in counts)
    palette = ("#2563eb", "#059669", "#7c3aed", "#ea580c")
    elements = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{html.escape(run["date"])} 项目领域分布</title>',
        f'<desc id="desc">共 {len(run["projects"])} 个项目，覆盖 {len(counts)} 个领域。</desc>',
        '<rect width="100%" height="100%" fill="#f8fafc" rx="16"/>',
        f'<text x="32" y="42" font-family="system-ui,sans-serif" font-size="24" font-weight="700" fill="#0f172a">GitHub 世界雷达 · {html.escape(run["date"])}</text>',
        '<text x="32" y="68" font-family="system-ui,sans-serif" font-size="14" fill="#475569">项目领域分布（按本期收录数）</text>',
    ]
    for index, (domain, count) in enumerate(counts):
        y = top + index * row_height
        bar_width = max(12, round(max_bar * count / maximum))
        color = palette[index % len(palette)]
        elements.extend(
            [
                f'<text x="32" y="{y + 21}" font-family="system-ui,sans-serif" font-size="14" fill="#1e293b">{html.escape(domain)}</text>',
                f'<rect x="{label_width}" y="{y + 4}" width="{bar_width}" height="24" rx="6" fill="{color}"/>',
                f'<text x="{label_width + bar_width + 10}" y="{y + 22}" font-family="system-ui,sans-serif" font-size="14" font-weight="700" fill="#0f172a">{count}</text>',
            ]
        )
    elements.extend(
        [
            f'<text x="32" y="{height - 20}" font-family="system-ui,sans-serif" font-size="12" fill="#64748b">Run: {html.escape(run["run_id"])}</text>',
            "</svg>",
            "",
        ]
    )
    return "\n".join(elements)


def _render_signal_svg(run: Mapping[str, Any]) -> str:
    """Render a deterministic SVG chart of latest change-signal classifications."""

    counts = sorted(
        Counter(project["change_type"] for project in run["projects"]).items(),
        key=lambda item: (-item[1], item[0]),
    )
    width = 960
    row_height = 42
    top = 92
    height = top + row_height * len(counts) + 48
    label_width = 245
    maximum = max(count for _, count in counts)
    elements = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{html.escape(run["date"])} 变化信号分布</title>',
        f'<desc id="desc">共 {len(run["projects"])} 个项目，包含 {len(counts)} 类变化信号。</desc>',
        '<rect width="100%" height="100%" fill="#f8fafc" rx="16"/>',
        f'<text x="32" y="42" font-family="system-ui,sans-serif" font-size="24" font-weight="700" fill="#0f172a">GitHub 世界雷达 · {html.escape(run["date"])}</text>',
        '<text x="32" y="68" font-family="system-ui,sans-serif" font-size="14" fill="#475569">变化信号类型（按本期收录数）</text>',
    ]
    for index, (signal, count) in enumerate(counts):
        y = top + index * row_height
        bar_width = max(12, round(610 * count / maximum))
        color = ("#0f766e", "#4338ca", "#b45309", "#be123c")[index % 4]
        elements.extend(
            [
                f'<text x="32" y="{y + 21}" font-family="system-ui,sans-serif" font-size="14" fill="#1e293b">{html.escape(CHANGE_TYPES[signal])}</text>',
                f'<rect x="{label_width}" y="{y + 4}" width="{bar_width}" height="24" rx="6" fill="{color}"/>',
                f'<text x="{label_width + bar_width + 10}" y="{y + 22}" font-family="system-ui,sans-serif" font-size="14" font-weight="700" fill="#0f172a">{count}</text>',
            ]
        )
    elements.extend(
        [
            f'<text x="32" y="{height - 20}" font-family="system-ui,sans-serif" font-size="12" fill="#64748b">Run: {html.escape(run["run_id"])}</text>',
            "</svg>",
            "",
        ]
    )
    return "\n".join(elements)


def build_artifacts(runs: Sequence[Mapping[str, Any]]) -> list[Artifact]:
    """Construct every expected generated artifact without touching the filesystem."""

    if not runs:
        raise RadarError("at least one run is required")
    artifacts: list[Artifact] = []
    observations: dict[str, list[tuple[Mapping[str, Any], Mapping[str, Any]]]] = defaultdict(list)
    for run in runs:
        artifacts.append(Artifact(f"docs/daily/{run['date']}.md", _render_daily(run)))
        artifacts.append(Artifact(f"docs/assets/trends-{run['date']}.svg", _render_svg(run)))
        artifacts.append(Artifact(f"docs/assets/signals-{run['date']}.svg", _render_signal_svg(run)))
        for project in run["projects"]:
            observations[project["repository"].lower()].append((run, project))
    for key in sorted(observations):
        repository = observations[key][-1][1]["repository"]
        artifacts.append(
            Artifact(f"docs/projects/{_project_slug(repository)}.md", _render_project(repository, observations[key]))
        )
    latest = _latest_observations(runs)
    rising = [item for item in latest if item[1]["change_type"] in {"rising", "major_progress"}]
    surprising = [item for item in latest if item[1]["category"] == "surprising_and_experimental"]
    artifacts.extend(
        [
            Artifact("docs/index.md", _render_index(runs)),
            Artifact("data/generated/README-radar.md", _render_readme_fragment(runs)),
            Artifact("docs/indexes/domains.md", _render_domain_index(latest)),
            Artifact(
                "docs/indexes/rising.md",
                _render_project_index("升温项目", "最近一次观察中明显升温或取得重大进展的项目。", rising),
            ),
            Artifact(
                "docs/indexes/surprising.md",
                _render_project_index("意外发现", "容易被普通热门榜忽略、但能扩大认知边界的项目。", surprising),
            ),
        ]
    )
    paths = [artifact.path for artifact in artifacts]
    if len(paths) != len(set(paths)):
        raise RadarError("generator produced duplicate artifact paths")
    return sorted(artifacts, key=lambda artifact: artifact.path)


def _atomic_write(path: Path, content: str) -> None:
    """Atomically replace one UTF-8 text artifact after creating its directory."""

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            os.fchmod(handle.fileno(), 0o644)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def write_artifacts(repo: Path, artifacts: Iterable[Artifact]) -> list[str]:
    """Write changed artifacts atomically and return repository-relative paths changed."""

    changed: list[str] = []
    for artifact in artifacts:
        path = safe_path(repo, artifact.path)
        existing = path.read_text(encoding="utf-8") if path.is_file() else None
        if existing == artifact.content:
            continue
        _atomic_write(path, artifact.content)
        changed.append(artifact.path)
    return changed


def sync_readme(repo: Path, fragment: str) -> bool:
    """Replace the single generated README block and report whether it changed."""

    path = safe_path(repo, "README.md")
    if not path.is_file() or path.is_symlink():
        raise RadarError("README.md must be a regular non-symlink file")
    existing = path.read_text(encoding="utf-8")
    if existing.count(README_START) != 1 or existing.count(README_END) != 1:
        raise RadarError("README.md must contain exactly one generated marker pair")
    start = existing.index(README_START)
    end = existing.index(README_END, start) + len(README_END)
    replacement = fragment.strip()
    if not replacement.startswith(README_START) or not replacement.endswith(README_END):
        raise RadarError("generated README fragment has invalid markers")
    updated = existing[:start] + replacement + existing[end:]
    if updated == existing:
        return False
    _atomic_write(path, updated)
    return True


def validate_readme(repo: Path, fragment: str) -> list[str]:
    """Verify that README embeds the exact deterministic generated block."""

    path = safe_path(repo, "README.md")
    if not path.is_file() or path.is_symlink():
        return ["README.md must be a regular non-symlink file"]
    try:
        existing = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"cannot read README.md: {exc}"]
    if existing.count(README_START) != 1 or existing.count(README_END) != 1:
        return ["README.md must contain exactly one generated marker pair"]
    start = existing.index(README_START)
    end = existing.index(README_END, start) + len(README_END)
    if existing[start:end] != fragment.strip():
        return ["README.md generated block is stale"]
    return []


def _generated_files(repo: Path) -> set[str]:
    """List files below generator-owned roots without following escaped symlinks."""

    found: set[str] = set()
    resolved_repo = repo.resolve()
    for root_name in GENERATED_ROOTS:
        root = safe_path(repo, root_name)
        if not root.exists():
            continue
        if not root.is_dir():
            raise RadarError(f"generated root is not a directory: {root_name}")
        for path in root.rglob("*"):
            if path.is_symlink():
                raise RadarError(f"generated content must not be a symlink: {path.relative_to(resolved_repo)}")
            if path.is_file():
                found.add(path.relative_to(resolved_repo).as_posix())
    index = safe_path(repo, "docs/index.md")
    if index.is_file():
        found.add("docs/index.md")
    return found


def _validate_internal_links(repo: Path, artifacts: Sequence[Artifact]) -> list[str]:
    """Check relative Markdown links in generated artifacts against the expected output set."""

    expected = {artifact.path for artifact in artifacts}
    errors: list[str] = []
    link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for artifact in artifacts:
        if artifact.path == "data/generated/README-radar.md":
            # This fragment is validated as if embedded at repository-root README.md.
            parent = Path(".")
        else:
            parent = Path(artifact.path).parent
        for target in link_pattern.findall(artifact.content):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean_target = target.split("#", 1)[0]
            normalized = (parent / clean_target).as_posix()
            normalized_parts: list[str] = []
            for part in Path(normalized).parts:
                if part == "..":
                    if not normalized_parts:
                        errors.append(f"{artifact.path}: link escapes repository: {target}")
                        break
                    normalized_parts.pop()
                elif part not in {"", "."}:
                    normalized_parts.append(part)
            else:
                resolved = "/".join(normalized_parts)
                if resolved not in expected and not safe_path(repo, resolved).is_file():
                    errors.append(f"{artifact.path}: missing link target: {target}")
    return errors


def validate_artifacts(repo: Path, artifacts: Sequence[Artifact]) -> list[str]:
    """Compare generated files to expected content and report stale, missing, or extra output."""

    errors: list[str] = []
    expected = {artifact.path: artifact.content for artifact in artifacts}
    for relative, content in expected.items():
        path = safe_path(repo, relative)
        if not path.is_file():
            errors.append(f"missing generated artifact: {relative}")
            continue
        try:
            actual = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"cannot read {relative}: {exc}")
            continue
        if actual != content:
            digest = hashlib.sha256(actual.encode("utf-8")).hexdigest()[:12]
            errors.append(f"stale generated artifact: {relative} (actual sha256:{digest})")
    extras = _generated_files(repo) - set(expected)
    errors.extend(f"unexpected generated artifact: {relative}" for relative in sorted(extras))
    errors.extend(_validate_internal_links(repo, artifacts))
    return errors


def _repo_from_argument(value: str) -> Path:
    """Resolve and validate the requested repository root."""

    repo = Path(value).expanduser().resolve()
    if not repo.is_dir():
        raise RadarError(f"repository path is not a directory: {repo}")
    return repo


def main(argv: Sequence[str] | None = None) -> int:
    """Run the build or read-only validation command and return a process status."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "validate"))
    parser.add_argument("--repo", default=".", help="repository root (default: current directory)")
    args = parser.parse_args(argv)
    try:
        repo = _repo_from_argument(args.repo)
        runs = load_runs(repo)
        artifacts = build_artifacts(runs)
        readme_fragment = next(
            artifact.content for artifact in artifacts if artifact.path == "data/generated/README-radar.md"
        )
        if args.command == "build":
            changed = write_artifacts(repo, artifacts)
            if sync_readme(repo, readme_fragment):
                changed.append("README.md")
            errors = validate_artifacts(repo, artifacts) + validate_readme(repo, readme_fragment)
            if errors:
                raise RadarError("post-build validation failed:\n- " + "\n- ".join(errors))
            print(json.dumps({"status": "ok", "changed": changed}, ensure_ascii=False, sort_keys=True))
            return 0
        errors = validate_artifacts(repo, artifacts) + validate_readme(repo, readme_fragment)
        if errors:
            raise RadarError("validation failed:\n- " + "\n- ".join(errors))
        print(json.dumps({"status": "ok", "artifacts": len(artifacts)}, ensure_ascii=False, sort_keys=True))
        return 0
    except RadarError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

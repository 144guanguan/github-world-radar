"""Unit tests for deterministic radar generation and safety validation."""

from __future__ import annotations

import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from scripts.radar_builder import (
    RadarError,
    build_artifacts,
    load_runs,
    safe_path,
    sync_readme,
    validate_artifacts,
    validate_readme,
    validate_run,
    write_artifacts,
)


def sample_run() -> dict:
    """Return a fresh, schema-valid test run document."""

    return {
        "schema_version": 1,
        "run_id": "daily-2026-08-25",
        "date": "2026-08-25",
        "generated_at": "2026-08-25T08:30:00+08:00",
        "window": {"start": "2026-08-24", "end": "2026-08-25"},
        "summary": "开放科学与创作工具正在形成新的跨领域连接。",
        "trends": ["开放数据正在进入普通人的创作流程", "小型硬件项目更强调可复现性"],
        "projects": [
            {
                "repository": "octocat/Hello-World",
                "url": "https://github.com/octocat/Hello-World",
                "domain": "开放协作",
                "description": "一个用于验证协作流程的公开项目。",
                "why_now": "近期重新出现了活跃协作信号。",
                "signal": "最近提交和讨论均有更新。",
                "stage": "stable_development",
                "confidence": "high",
                "stars": 42,
                "forks": 7,
                "last_activity": "2026-08-24",
                "license": "MIT",
                "sources": [
                    {
                        "label": "仓库主页",
                        "url": "https://github.com/octocat/Hello-World",
                        "checked_at": "2026-08-25T08:00:00+08:00",
                    }
                ],
            }
        ],
    }


class RunValidationTests(unittest.TestCase):
    """Exercise input schema, duplicate, URL, and date validation."""

    def test_valid_run_is_normalized(self) -> None:
        """A complete run should validate without losing known fields."""

        validated = validate_run(sample_run())
        self.assertEqual(validated["projects"][0]["stars"], 42)
        self.assertEqual(validated["date"], "2026-08-25")

    def test_canonical_first_run_contract_is_normalized(self) -> None:
        """Canonical nested metrics, momentum, and evidence fields should be accepted."""

        raw = sample_run()
        project = raw["projects"][0]
        project.update(
            {
                "repo_id": 1296269,
                "full_name": project.pop("repository"),
                "tags": ["协作", "示例"],
                "category": "surprising_and_experimental",
                "change_type": "rising",
                "summary": project.pop("description"),
                "what_it_signals": project.pop("signal"),
                "metrics": {
                    "stars": project.pop("stars"),
                    "forks": project.pop("forks"),
                    "contributors": None,
                    "latest_commit_at": "2026-08-24T12:00:00Z",
                    "latest_release_at": None,
                    "license": project.pop("license"),
                },
                "momentum": {"stars_7d": None, "stars_30d": 10, "proxy_signals": ["讨论增加"]},
                "evidence": [
                    {
                        "type": "repository",
                        "url": "https://github.com/octocat/Hello-World",
                        "observed_at": "2026-08-25T08:00:00+08:00",
                    }
                ],
                "risks": ["精确七日增量不可得"],
                "recommended_action": "持续跟踪",
            }
        )
        project.pop("sources")
        project.pop("last_activity")
        validated = validate_run(raw)
        self.assertEqual(validated["projects"][0]["repository"], "octocat/Hello-World")
        self.assertEqual(validated["projects"][0]["repo_id"], "1296269")
        self.assertEqual(validated["projects"][0]["stars_30d"], 10)
        self.assertEqual(validated["projects"][0]["change_type"], "rising")

    def test_duplicate_repository_is_rejected_case_insensitively(self) -> None:
        """The same repository cannot occur twice in one report."""

        raw = sample_run()
        duplicate = deepcopy(raw["projects"][0])
        duplicate["repository"] = "OctoCat/hello-world"
        duplicate["url"] = "https://github.com/OctoCat/hello-world"
        raw["projects"].append(duplicate)
        with self.assertRaisesRegex(RadarError, "duplicate repositories"):
            validate_run(raw)

    def test_repository_url_must_match_repository(self) -> None:
        """A project cannot point readers to another GitHub repository."""

        raw = sample_run()
        raw["projects"][0]["url"] = "https://github.com/other/project"
        with self.assertRaisesRegex(RadarError, "must equal"):
            validate_run(raw)

    def test_sensitive_query_parameter_is_rejected(self) -> None:
        """Evidence links must not persist access tokens or signed URLs."""

        raw = sample_run()
        raw["projects"][0]["sources"][0]["url"] = "https://example.com/evidence?token=secret"
        with self.assertRaisesRegex(RadarError, "sensitive query"):
            validate_run(raw)

    def test_timezone_is_required(self) -> None:
        """Generated timestamps must be unambiguous across daily runs."""

        raw = sample_run()
        raw["generated_at"] = "2026-08-25T08:30:00"
        with self.assertRaisesRegex(RadarError, "timezone"):
            validate_run(raw)


class ArtifactTests(unittest.TestCase):
    """Exercise deterministic rendering, safe writes, and artifact checks."""

    def setUp(self) -> None:
        """Create an isolated repository-shaped directory for each test."""

        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name)
        (self.repo / "data" / "runs").mkdir(parents=True)
        (self.repo / "data" / "runs" / "2026-08-25.json").write_text(
            json.dumps(sample_run(), ensure_ascii=False), encoding="utf-8"
        )
        (self.repo / "README.md").write_text(
            "# Radar\n\n<!-- RADAR:GENERATED:START -->\nold\n<!-- RADAR:GENERATED:END -->\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        """Dispose of the isolated test directory."""

        self.temporary.cleanup()

    def test_build_is_deterministic_and_idempotent(self) -> None:
        """Equivalent input should yield byte-identical output and no second write."""

        runs = load_runs(self.repo)
        first = build_artifacts(runs)
        second = build_artifacts(runs)
        self.assertEqual(first, second)
        changed = write_artifacts(self.repo, first)
        self.assertTrue(changed)
        self.assertEqual(write_artifacts(self.repo, second), [])
        self.assertEqual(validate_artifacts(self.repo, second), [])

    def test_expected_artifact_set_contains_report_profile_index_fragment_and_svg(self) -> None:
        """One run should produce every public navigation and visual artifact."""

        paths = {artifact.path for artifact in build_artifacts(load_runs(self.repo))}
        self.assertEqual(
            paths,
            {
                "docs/assets/trends-2026-08-25.svg",
                "docs/assets/signals-2026-08-25.svg",
                "docs/daily/2026-08-25.md",
                "data/generated/README-radar.md",
                "docs/index.md",
                "docs/indexes/domains.md",
                "docs/indexes/rising.md",
                "docs/indexes/surprising.md",
                "docs/projects/octocat--Hello-World.md",
            },
        )

    def test_validation_detects_stale_and_extra_generated_files(self) -> None:
        """Read-only validation should flag drift and abandoned generated files."""

        artifacts = build_artifacts(load_runs(self.repo))
        write_artifacts(self.repo, artifacts)
        (self.repo / "docs" / "daily" / "2026-08-25.md").write_text("stale", encoding="utf-8")
        (self.repo / "docs" / "projects" / "extra.md").write_text("extra", encoding="utf-8")
        errors = validate_artifacts(self.repo, artifacts)
        self.assertTrue(any("stale generated artifact" in error for error in errors))
        self.assertTrue(any("unexpected generated artifact" in error for error in errors))

    def test_safe_path_rejects_parent_traversal(self) -> None:
        """Repository writes cannot escape through parent path segments."""

        with self.assertRaisesRegex(RadarError, "unsafe"):
            safe_path(self.repo, "../outside.md")

    def test_safe_path_rejects_symlink_escape(self) -> None:
        """Repository writes cannot escape through a generated-root symlink."""

        outside = Path(self.temporary.name).parent / f"{Path(self.temporary.name).name}-outside"
        outside.mkdir(exist_ok=True)
        try:
            (self.repo / "docs").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(RadarError, "escapes repository"):
                safe_path(self.repo, "docs/index.md")
        finally:
            outside.rmdir()

    def test_duplicate_run_date_is_rejected(self) -> None:
        """Two files cannot silently compete for the same daily output path."""

        second = sample_run()
        second["run_id"] = "retry-2026-08-25"
        (self.repo / "data" / "runs" / "retry.json").write_text(json.dumps(second), encoding="utf-8")
        with self.assertRaisesRegex(RadarError, "same date"):
            load_runs(self.repo)

    def test_readme_generated_block_is_synced_idempotently(self) -> None:
        """README should update only its generated block and become stable."""

        artifacts = build_artifacts(load_runs(self.repo))
        fragment = next(item.content for item in artifacts if item.path == "data/generated/README-radar.md")
        self.assertTrue(sync_readme(self.repo, fragment))
        self.assertFalse(sync_readme(self.repo, fragment))
        self.assertEqual(validate_readme(self.repo, fragment), [])
        self.assertTrue((self.repo / "README.md").read_text(encoding="utf-8").startswith("# Radar"))


if __name__ == "__main__":
    unittest.main()

---
title: "liketrek/TREK"
description: "项目方称其为可自托管、实时协作的旅行规划器，结合地图、预算、清单和旅行日记。"
---
# [liketrek/TREK](https://github.com/liketrek/TREK)

项目方称其为可自托管、实时协作的旅行规划器，结合地图、预算、清单和旅行日记。

## 当前快照

- 领域：个人生活与生产力
- 阶段：快速成长
- 置信度：高
- Stars：13,004
- Forks：1,127
- 最近活动：2026-08-29
- License：AGPL-3.0
- 稳定标识：`1186219527`
- 变化类型：新进入视野
- 发现类别：明确势头
- 7 日 Star 增量：数据不可得
- 30 日 Star 增量：数据不可得
- 推荐行动：阅读 v4.1.1 的故障解释，以不含真实地址的示例行程理解外部服务依赖；持续跟踪下一补丁后再考虑导入私人数据。
- 最近收录：[日报 2026-08-31](../daily/2026-08-31.md)

## 为什么值得关注

2026-08-29 发布 v4.1.1，修复 v4.1.0 默认矢量底图缺少 zoom 上限导致行程页与地图设置打不开的阻断故障，并处理地点重复判断和住宿日历问题。

公开信号：推断：旅行记录可自托管，底图与地理编码仍依赖外部服务；TREK 修复与 TRIP 1.49.0 切换默认瓦片提供商的同期事件，提示应将这些依赖视为产品可靠性的一部分。

## 证据

- [repository](https://github.com/liketrek/TREK)（核验于 `2026-08-31T10:04:39+08:00`）
- [readme](https://github.com/liketrek/TREK/blob/main/README.md)（核验于 `2026-08-31T10:04:39+08:00`）
- [commit](https://github.com/liketrek/TREK/commit/33a33e7b1d113f0742ac609305cc549a4806d31b)（核验于 `2026-08-31T10:04:39+08:00`）
- [release](https://github.com/liketrek/TREK/releases/tag/v4.1.1)（核验于 `2026-08-31T10:04:39+08:00`）
- [issue](https://github.com/liketrek/TREK/issues/2135)（核验于 `2026-08-31T10:04:39+08:00`）
- [pull_request](https://github.com/liketrek/TREK/pull/2161)（核验于 `2026-08-31T10:04:39+08:00`）
- [cross_project_release](https://github.com/itskovacs/trip/releases/tag/1.49.0)（核验于 `2026-08-31T10:04:39+08:00`）
- [license](https://github.com/liketrek/TREK/blob/main/LICENSE)（核验于 `2026-08-31T10:04:39+08:00`）
- [repository_api](https://api.github.com/repos/liketrek/TREK)（核验于 `2026-08-31T11:03:15+08:00`）

## 观察历史

- [2026-08-31](../daily/2026-08-31.md)：推断：旅行记录可自托管，底图与地理编码仍依赖外部服务；TREK 修复与 TRIP 1.49.0 切换默认瓦片提供商的同期事件，提示应将这些依赖视为产品可靠性的一部分。（快速成长）

## 标签

`travel` · `self-hosted` · `maps` · `collaboration`

## 代理信号

- 2026-08-29 发布 v4.1.1 阻断故障补丁
- 用户报告 Issue #2135 同日关闭
- v4.1.2 PR #2161 尚未合并，不计为已发布能力

## 风险与边界

- 本轮未运行软件，发布说明与 Issue 关闭不足以证明所有环境已恢复稳定。
- 行程、住址、同行者及预算敏感；自托管不等于隐私已审计，可选插件和 AI/MCP 也扩大数据流向。
- 地图与地理编码服务有配额、隐私和授权条件，代码 AGPL 不替代地图数据许可。
- TRIP 维护者关于 CARTO 服务变化的原因尚未向供应商独立核实，仅引用其发布中的切换事实。

---
title: "CliMA/ClimaAtmos.jl"
description: "项目方称其为 CliMA 地球系统模型中的 GPU 全球大气模型，支持数据同化和机器学习校准。"
---
# [CliMA/ClimaAtmos.jl](https://github.com/CliMA/ClimaAtmos.jl)

项目方称其为 CliMA 地球系统模型中的 GPU 全球大气模型，支持数据同化和机器学习校准。

## 当前快照

- 领域：气候、能源与地球
- 阶段：稳定发展
- 置信度：高
- Stars：125
- Forks：37
- 最近活动：2026-08-27
- License：Apache-2.0
- 稳定标识：`377910358`
- 变化类型：新进入视野
- 发现类别：跨领域潜力
- 7 日 Star 增量：数据不可得
- 30 日 Star 增量：数据不可得
- 推荐行动：阅读该修复的测试与模型配置背景，理解一个小警告如何防止科学结果被错误边界条件污染。
- 最近收录：[日报 2026-08-28](../daily/2026-08-28.md)

## 为什么值得关注

2026-08-21 发布 v0.42.7；2026-08-27 最新提交为 SlabOceanSST 覆盖表面温度条件时增加明确警告并将测试接入 CI，属于影响科学配置正确性的实质修正。

公开信号：推断：成熟科学计算项目正在把隐式配置覆盖变成可观察、可回归验证的行为，模型可信度越来越依赖工程护栏。

## 证据

- [repository](https://github.com/CliMA/ClimaAtmos.jl)（核验于 `2026-08-28T11:22:58+08:00`）
- [readme](https://github.com/CliMA/ClimaAtmos.jl/blob/main/README.md)（核验于 `2026-08-28T11:22:58+08:00`）
- [commit](https://github.com/CliMA/ClimaAtmos.jl/commit/b0d865eab6beae66144c3cc6080b4c0cf9901e1f)（核验于 `2026-08-28T11:22:58+08:00`）
- [release](https://github.com/CliMA/ClimaAtmos.jl/releases/tag/v0.42.7)（核验于 `2026-08-28T11:22:58+08:00`）
- [license](https://github.com/CliMA/ClimaAtmos.jl/blob/main/LICENSE)（核验于 `2026-08-28T11:22:58+08:00`）

## 观察历史

- [2026-08-28](../daily/2026-08-28.md)：推断：成熟科学计算项目正在把隐式配置覆盖变成可观察、可回归验证的行为，模型可信度越来越依赖工程护栏。（稳定发展）

## 标签

`climate-model` · `atmosphere` · `gpu` · `scientific-computing`

## 代理信号

- 7 日内发布 v0.42.7
- 新增配置覆盖警告
- 新增并接入 CI 的回归测试

## 风险与边界

- 数值结果依赖参数、网格、初始条件、数据同化和硬件环境，仓库活跃不能替代科学验证。
- 最新修复包含 AI 辅助贡献记录，仍需按项目测试和科学审查流程判断可靠性。

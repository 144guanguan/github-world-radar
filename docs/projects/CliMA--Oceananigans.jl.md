---
title: "CliMA/Oceananigans.jl"
description: "项目方称其为可在 CPU 和 GPU 上运行的 Julia 海洋流体动力学模拟软件。"
---
# [CliMA/Oceananigans.jl](https://github.com/CliMA/Oceananigans.jl)

项目方称其为可在 CPU 和 GPU 上运行的 Julia 海洋流体动力学模拟软件。

## 当前快照

- 领域：气候、能源与地球
- 阶段：稳定发展
- 置信度：高
- Stars：1,412
- Forks：290
- 最近活动：2026-08-26
- License：MIT
- 稳定标识：`152878952`
- 变化类型：重大进展
- 发现类别：明确势头
- 7 日 Star 增量：数据不可得
- 30 日 Star 增量：数据不可得
- 推荐行动：阅读本次修复和回归测试，持续跟踪科学验证而非 Star 变化。
- 最近收录：[日报 2026-08-27](../daily/2026-08-27.md)

## 为什么值得关注

继昨日入选后，2026-08-26 又修复显式时间离散路径中的三个潜在错误并补充回归测试；Star 和 Fork 保持不变。

公开信号：推断：科研基础设施的真实进展常表现为边界条件、数值路径和回归测试的精细修复，而不是热度增长。

## 证据

- [repository](https://github.com/CliMA/Oceananigans.jl)（核验于 `2026-08-27T13:37:00+08:00`）
- [release](https://github.com/CliMA/Oceananigans.jl/releases/tag/v0.110.19)（核验于 `2026-08-27T13:37:00+08:00`）
- [commit](https://github.com/CliMA/Oceananigans.jl/commit/9685775fadbc2219b6f77cadc1b4af7498a8d08e)（核验于 `2026-08-27T13:37:00+08:00`）
- [pull_request](https://github.com/CliMA/Oceananigans.jl/pull/5896)（核验于 `2026-08-27T13:37:00+08:00`）

## 观察历史

- [2026-08-27](../daily/2026-08-27.md)：推断：科研基础设施的真实进展常表现为边界条件、数值路径和回归测试的精细修复，而不是热度增长。（稳定发展）
- [2026-08-26](../daily/2026-08-26.md)：推断：高性能科学模拟正在同时追求加速计算、可组合数据格式和更可复现的研究工作流。（稳定发展）

## 标签

`ocean-modeling` · `fluid-dynamics` · `julia` · `gpu`

## 代理信号

- 相邻快照 Star 和 Fork 均未变化
- 新增带回归测试的数值路径修复
- 六天内发布 v0.110.19

## 风险与边界

- 项目仍处于 0.x 版本，接口稳定性需要核验。
- 数值模拟需结合网格、边界条件、实验数据和独立复现验证。
- 不同硬件和精度设置可能影响可重复性。

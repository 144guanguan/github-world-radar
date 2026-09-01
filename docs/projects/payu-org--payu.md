---
title: "payu-org/payu"
description: "项目方称 Payu 是在澳大利亚 NCI 超级计算环境运行数值气候模型的工作流工具。"
---
# [payu-org/payu](https://github.com/payu-org/payu)

项目方称 Payu 是在澳大利亚 NCI 超级计算环境运行数值气候模型的工作流工具。

## 当前快照

- 领域：气候、能源与地球
- 阶段：稳定发展
- 置信度：高
- Stars：23
- Forks：30
- 最近活动：2026-09-01
- License：Apache-2.0
- 稳定标识：`2633574`
- 变化类型：新进入视野
- 发现类别：跨领域潜力
- 7 日 Star 增量：数据不可得
- 30 日 Star 增量：数据不可得
- 推荐行动：阅读背景：沿 restart 产物、溯源字段和作业依赖链理解气候模拟可重复性，不执行仓库代码。
- 最近收录：[日报 2026-09-01](../daily/2026-09-01.md)

## 为什么值得关注

2026-08-31 至 09-01 新增 restart 最小溯源、run 到 collate/postscript/sync 的依赖链，并在 repeat 模式检查已有 restart，避免长任务恢复时覆盖既有状态。

公开信号：推断：高成本气候模拟的可靠性不只取决于模型方程，也取决于任务能否恢复、产物能否追溯以及后处理依赖是否明确。

## 证据

- [repository](https://github.com/payu-org/payu)（核验于 `2026-09-01T11:09:00+08:00`）
- [repository_api](https://api.github.com/repos/payu-org/payu)（核验于 `2026-09-01T11:09:00+08:00`）
- [readme](https://github.com/payu-org/payu/blob/master/README.rst)（核验于 `2026-09-01T11:09:00+08:00`）
- [commit](https://github.com/payu-org/payu/commit/b6962f8d005a75a4f1158e9a2cf53d1003e465d0)（核验于 `2026-09-01T11:09:00+08:00`）
- [restart_provenance_commit](https://github.com/payu-org/payu/commit/30ec256efa37885a0ec8d31c637bd7783b7d1290)（核验于 `2026-09-01T11:09:00+08:00`）
- [release](https://github.com/payu-org/payu/releases/tag/1.3.5)（核验于 `2026-09-01T11:09:00+08:00`）
- [license_status](https://api.github.com/repos/payu-org/payu/license)（核验于 `2026-09-01T11:09:00+08:00`）

## 观察历史

- [2026-09-01](../daily/2026-09-01.md)：推断：高成本气候模拟的可靠性不只取决于模型方程，也取决于任务能否恢复、产物能否追溯以及后处理依赖是否明确。（稳定发展）

## 标签

`climate-modeling` · `hpc` · `workflow` · `provenance`

## 代理信号

- 窗口内连续改进 restart 防覆盖与溯源
- 补充高性能计算作业依赖链
- 低 Star 但面向专业气候模拟工作流

## 风险与边界

- README 明确当前配置面向澳大利亚 NCI，不能外推为通用 HPC 工作流。
- 本轮未在超级计算环境执行恢复流程，不能声称所有中断、并发和存储故障已解决。
- 最新正式 Release 是 2026-08-25 的 1.3.5，本期属于主线提交进展。

---
title: "nco/nco"
description: "项目方称其提供 netCDF/HDF/DAP 科学数据命令行算子，用于统计、重映射、气候平均与元数据处理。"
---
# [nco/nco](https://github.com/nco/nco)

项目方称其提供 netCDF/HDF/DAP 科学数据命令行算子，用于统计、重映射、气候平均与元数据处理。

## 当前快照

- 领域：气候、能源与地球
- 阶段：稳定发展
- 置信度：高
- Stars：197
- Forks：55
- 最近活动：2026-08-30
- License：未核验
- 稳定标识：`31292536`
- 变化类型：新进入视野
- 发现类别：跨领域潜力
- 7 日 Star 增量：数据不可得
- 30 日 Star 增量：数据不可得
- 推荐行动：阅读背景：了解 ncclimo 与 ncremap 如何处理时间及空间维度，跟踪下一正式版是否纳入 8 月 30 日的修复。
- 最近收录：[日报 2026-08-31](../daily/2026-08-31.md)

## 为什么值得关注

2026-08-30 的两个提交修复 ncremap/ncclimo 错误处理对常用命令的影响，最新提交针对时间序列命令误入错误处理器，涉及变量初始化和 shell 算术处理。

公开信号：推断：气候研究可重复性的基础条件，常藏在文件维度、时间切片和错误处理这些维护细节里；本次有实质修复证据，但没有爆红或数值精度提升的证据。

## 证据

- [repository](https://github.com/nco/nco)（核验于 `2026-08-31T10:04:37+08:00`）
- [readme](https://github.com/nco/nco/blob/master/README.md)（核验于 `2026-08-31T10:04:37+08:00`）
- [commit](https://github.com/nco/nco/commit/ad6b928356347e4accf22bfae0f6e8eebe67a659)（核验于 `2026-08-31T10:04:37+08:00`）
- [commit](https://github.com/nco/nco/commit/6edb83d2f45ff5421a1fe4e51564b3df5bd808a8)（核验于 `2026-08-31T10:04:37+08:00`）
- [pull_request](https://github.com/nco/nco/pull/315)（核验于 `2026-08-31T10:04:37+08:00`）
- [release](https://github.com/nco/nco/releases/tag/5.3.8)（核验于 `2026-08-31T10:04:37+08:00`）
- [license_status](https://api.github.com/repos/nco/nco/license)（核验于 `2026-08-31T10:04:37+08:00`）
- [license_file](https://github.com/nco/nco/blob/master/LICENSE)（核验于 `2026-08-31T10:04:37+08:00`）
- [license_terms](https://github.com/nco/nco/blob/master/COPYING)（核验于 `2026-08-31T10:04:37+08:00`）

## 观察历史

- [2026-08-31](../daily/2026-08-31.md)：推断：气候研究可重复性的基础条件，常藏在文件维度、时间切片和错误处理这些维护细节里；本次有实质修复证据，但没有爆红或数值精度提升的证据。（稳定发展）

## 标签

`climate` · `netcdf` · `scientific-data`

## 代理信号

- 2026-08-30 连续修复重映射与气候时间序列错误处理
- 最新正式 Release 仍为 5.3.8，主线修复尚未据此证实已正式交付
- 首次收录，无历史增长快照

## 风险与边界

- GitHub 自动许可证标识为 NOASSERTION，标准字段保留 null；LICENSE/COPYING 明确项目自创源码为 BSD-3-Clause，而 README 仍链接 GPL-3.0，存在口径不一致，并非没有许可证。
- 依赖库另有授权要求；使用前需按具体版本与文件核对。
- 未执行数据处理或复现修复，结果仍依赖坐标、单位和时间维度；PR #315 尚未合并，不将相关撤销链当稳定功能。

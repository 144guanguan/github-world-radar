---
title: "catalyst-cooperative/pudl"
description: "项目方称 PUDL 将美国公共事业和能源系统数据整理为可分析数据，服务气候倡议者、研究者、政策制定者和记者。"
---
# [catalyst-cooperative/pudl](https://github.com/catalyst-cooperative/pudl)

项目方称 PUDL 将美国公共事业和能源系统数据整理为可分析数据，服务气候倡议者、研究者、政策制定者和记者。

## 当前快照

- 领域：气候、能源与地球
- 阶段：稳定发展
- 置信度：高
- Stars：602
- Forks：144
- 最近活动：2026-08-31
- License：MIT
- 稳定标识：`80646423`
- 变化类型：重大进展
- 发现类别：跨领域潜力
- 7 日 Star 增量：数据不可得
- 30 日 Star 增量：数据不可得
- 推荐行动：持续跟踪：阅读 PR #5442 的异常处理和测试，对照一个 FERC EQR 季度理解缺失申报如何被记录。
- 最近收录：[日报 2026-09-01](../daily/2026-09-01.md)

## 为什么值得关注

2026-08-31 合并 FERC EQR 数据正确性修复：允许不完整或不可解析的申报、保留 ENUM 类型、清除归档刷新后遗留的陈旧 Parquet，并补充季度提取统计和测试。

公开信号：推断：能源开放数据的关键进展常是诚实处理缺失、损坏和旧缓存，而不是简单增加数据量；错误状态可见才能支撑可复核分析。

## 证据

- [repository](https://github.com/catalyst-cooperative/pudl)（核验于 `2026-09-01T11:09:00+08:00`）
- [repository_api](https://api.github.com/repos/catalyst-cooperative/pudl)（核验于 `2026-09-01T11:09:00+08:00`）
- [readme](https://github.com/catalyst-cooperative/pudl/blob/main/README.rst)（核验于 `2026-09-01T11:09:00+08:00`）
- [commit](https://github.com/catalyst-cooperative/pudl/commit/c33227708024fd718d30cb52a9b85e774d5fd1a0)（核验于 `2026-09-01T11:09:00+08:00`）
- [pull_request](https://github.com/catalyst-cooperative/pudl/pull/5442)（核验于 `2026-09-01T11:09:00+08:00`）
- [release](https://github.com/catalyst-cooperative/pudl/releases/tag/v2026.8.0)（核验于 `2026-09-01T11:09:00+08:00`）
- [license](https://github.com/catalyst-cooperative/pudl/blob/main/LICENSE.txt)（核验于 `2026-09-01T11:09:00+08:00`）

## 观察历史

- [2026-09-01](../daily/2026-09-01.md)：推断：能源开放数据的关键进展常是诚实处理缺失、损坏和旧缓存，而不是简单增加数据量；错误状态可见才能支撑可复核分析。（稳定发展）
- [2026-08-29](../daily/2026-08-29.md)：推断：气候与能源研究的关键进展常来自数据口径、版本和 ETL 修正，而不是新的可视化界面。（稳定发展）

## 标签

`energy-data` · `ferc` · `data-quality` · `regulatory-data`

## 代理信号

- 2026-08-31 合并 FERC EQR 不完整申报与陈旧文件修复
- 2026-08-29 至 09-01 两次观测均为 602 Star、144 Fork；只是 3 日差值
- 当前仍有跨季度诊断和多年份状态修复 PR，尚未合并

## 风险与边界

- 上游 FERC 申报可能缺失、损坏或后续修订；PUDL 是加工数据，不是原始监管记录。
- 关键研究应固定数据版本、来源季度、异常统计和清洗规则，不能把成功运行等同于数据无误。
- 本轮只核验变更和公开测试内容，未执行数据管线或复算结果。

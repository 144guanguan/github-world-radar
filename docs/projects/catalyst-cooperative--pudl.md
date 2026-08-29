---
title: "catalyst-cooperative/pudl"
description: "项目方称 PUDL 把美国政府公用事业和能源数据加工成可分析、可版本化的数据资源。"
---
# [catalyst-cooperative/pudl](https://github.com/catalyst-cooperative/pudl)

项目方称 PUDL 把美国政府公用事业和能源数据加工成可分析、可版本化的数据资源。

## 当前快照

- 领域：气候、能源与地球
- 阶段：稳定发展
- 置信度：高
- Stars：602
- Forks：144
- 最近活动：2026-08-28
- License：MIT
- 稳定标识：`80646423`
- 变化类型：新进入视野
- 发现类别：跨领域潜力
- 7 日 Star 增量：数据不可得
- 30 日 Star 增量：数据不可得
- 推荐行动：阅读数据修复 PR，理解能源研究中版本化 ETL 为什么比单次下载更重要。
- 最近收录：[日报 2026-08-29](../daily/2026-08-29.md)

## 为什么值得关注

2026-08-28 更新测试重组后的文档，并持续处理发电燃料多年度分配错误和 NREL ATB 新分区格式，直接影响能源数据复现。

公开信号：推断：气候与能源研究的关键进展常来自数据口径、版本和 ETL 修正，而不是新的可视化界面。

## 证据

- [repository](https://github.com/catalyst-cooperative/pudl)（核验于 `2026-08-29T11:08:13+08:00`）
- [readme](https://github.com/catalyst-cooperative/pudl/blob/30b2e6749c507b1173b828f6f243e1a78d959af3/README.rst)（核验于 `2026-08-29T11:08:13+08:00`）
- [commit](https://github.com/catalyst-cooperative/pudl/commit/30b2e6749c507b1173b828f6f243e1a78d959af3)（核验于 `2026-08-29T11:08:13+08:00`）
- [release](https://github.com/catalyst-cooperative/pudl/releases/tag/v2026.8.0)（核验于 `2026-08-29T11:08:13+08:00`）
- [pull_request](https://github.com/catalyst-cooperative/pudl/pull/5511)（核验于 `2026-08-29T11:08:13+08:00`）
- [license](https://github.com/catalyst-cooperative/pudl/blob/main/LICENSE.txt)（核验于 `2026-08-29T11:08:13+08:00`）

## 观察历史

- [2026-08-29](../daily/2026-08-29.md)：推断：气候与能源研究的关键进展常来自数据口径、版本和 ETL 修正，而不是新的可视化界面。（稳定发展）

## 标签

`energy-data` · `open-data` · `etl` · `public-utilities`

## 代理信号

- 持续修复多年度燃料分配
- 适配 NREL ATB 新分区格式
- 2026-08-28 补齐测试文档

## 风险与边界

- 政府源数据可能滞后、修订或改变字段定义，ETL 错误会传播到下游分析。
- 不能把该数据直接当作实时电网运行、交易、监管或政策结论。
- 复现时必须保留具体数据版本、处理代码和 DOI。

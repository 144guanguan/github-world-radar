---
title: "AlertaDengue/PySUS"
description: "项目方称其用于下载、清理和分析巴西统一卫生系统的开放数据，并统一访问 DATASUS、dados.gov.br、OpenDataSUS 等来源。"
---
# [AlertaDengue/PySUS](https://github.com/AlertaDengue/PySUS)

项目方称其用于下载、清理和分析巴西统一卫生系统的开放数据，并统一访问 DATASUS、dados.gov.br、OpenDataSUS 等来源。

## 当前快照

- 领域：医疗健康与生命科学
- 阶段：稳定发展
- 置信度：高
- Stars：246
- Forks：95
- 最近活动：2026-09-01
- License：GPL-3.0
- 稳定标识：`63720586`
- 变化类型：新进入视野
- 发现类别：明确势头
- 7 日 Star 增量：数据不可得
- 30 日 Star 增量：数据不可得
- 推荐行动：阅读 2.11.0 变更和来源命名空间设计；若用于研究，先用一项公开指标对照官方原始表并记录查询日期。
- 最近收录：[日报 2026-09-01](../daily/2026-09-01.md)

## 为什么值得关注

2026-09-01 发布 2.11.0；相邻提交把不同公共卫生数据源拆成显式模块，使调用者可以辨认数据来自哪个系统，而不是把所有数据隐藏在一个入口后。

公开信号：推断：公共卫生数据工具的竞争点正在从能否下载，转向来源是否可见、数据质量是否可解释以及查询过程能否复核。

## 证据

- [repository](https://github.com/AlertaDengue/PySUS)（核验于 `2026-09-01T11:09:00+08:00`）
- [repository_api](https://api.github.com/repos/AlertaDengue/PySUS)（核验于 `2026-09-01T11:09:00+08:00`）
- [readme](https://github.com/AlertaDengue/PySUS/blob/main/README.md)（核验于 `2026-09-01T11:09:00+08:00`）
- [commit](https://github.com/AlertaDengue/PySUS/commit/b423222cfe25727d723cbdbc9a31bacd49159e6f)（核验于 `2026-09-01T11:09:00+08:00`）
- [source_modules_commit](https://github.com/AlertaDengue/PySUS/commit/38f4152f0f4c8cd1e77c7c8b8a194c8e11f2c215)（核验于 `2026-09-01T11:09:00+08:00`）
- [release](https://github.com/AlertaDengue/PySUS/releases/tag/2.11.0)（核验于 `2026-09-01T11:09:00+08:00`）
- [license](https://api.github.com/repos/AlertaDengue/PySUS/license)（核验于 `2026-09-01T11:09:00+08:00`）

## 观察历史

- [2026-09-01](../daily/2026-09-01.md)：推断：公共卫生数据工具的竞争点正在从能否下载，转向来源是否可见、数据质量是否可解释以及查询过程能否复核。（稳定发展）

## 标签

`public-health` · `open-data` · `brazil` · `provenance`

## 代理信号

- 2026-09-01 发布正式版 2.11.0
- 发布前提交显式拆分公共卫生数据来源
- 首次收录，没有可复核的 7 日或 30 日增长端点

## 风险与边界

- 数据完整性、延迟和修订仍取决于巴西公共数据源；工具输出不能直接替代医疗或公共卫生专业判断。
- 本轮未抽样核对下载结果与官方原始记录，也未验证所有地区和年份的覆盖。
- GPL-3.0 对再分发和集成有义务，数据本身的使用条款还需按来源分别检查。

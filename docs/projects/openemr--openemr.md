---
title: "openemr/openemr"
description: "项目方称其为开源电子病历与诊所管理系统，覆盖排班、账单、国际化、API 和 FHIR。"
---
# [openemr/openemr](https://github.com/openemr/openemr)

项目方称其为开源电子病历与诊所管理系统，覆盖排班、账单、国际化、API 和 FHIR。

## 当前快照

- 领域：医疗健康与生命科学
- 阶段：成熟项目重新升温
- 置信度：高
- Stars：5,399
- Forks：3,017
- 最近活动：2026-08-28
- License：GPL-3.0
- 稳定标识：`679584`
- 变化类型：新进入视野
- 发现类别：明确势头
- 7 日 Star 增量：数据不可得
- 30 日 Star 增量：数据不可得
- 推荐行动：阅读 8.3.0 的升级与安全文档，并把它作为医疗软件长期治理的案例而非即装即用方案。
- 最近收录：[日报 2026-08-28](../daily/2026-08-28.md)

## 为什么值得关注

OpenEMR 8.3.0 于 2026-08-18 发布；2026-08-28 的最新提交继续重构模板依赖，并把参数错误页面从隐式 HTTP 200 修正为 400。

公开信号：推断：长期医疗软件仍在通过细小但关键的协议语义和依赖治理修复来降低集成歧义，而不只是追逐新功能。

## 证据

- [repository](https://github.com/openemr/openemr)（核验于 `2026-08-28T11:22:58+08:00`）
- [readme](https://github.com/openemr/openemr/blob/master/README.md)（核验于 `2026-08-28T11:22:58+08:00`）
- [commit](https://github.com/openemr/openemr/commit/94fbfe374e2a44de1c816bb2d681f5578c81f446)（核验于 `2026-08-28T11:22:58+08:00`）
- [release](https://github.com/openemr/openemr/releases/tag/v8_3_0)（核验于 `2026-08-28T11:22:58+08:00`）
- [license](https://github.com/openemr/openemr/blob/master/LICENSE)（核验于 `2026-08-28T11:22:58+08:00`）

## 观察历史

- [2026-08-28](../daily/2026-08-28.md)：推断：长期医疗软件仍在通过细小但关键的协议语义和依赖治理修复来降低集成歧义，而不只是追逐新功能。（成熟项目重新升温）

## 标签

`electronic-health-record` · `fhir` · `medical-practice` · `healthcare`

## 代理信号

- 10 日前发布 8.3.0
- 发布后持续架构改造
- 修正错误响应的 HTTP 状态语义

## 风险与边界

- 医疗软件涉及患者隐私、权限、审计、法规和临床安全，未经机构级评估不可直接用于真实医疗环境。
- 仓库活动和通用功能不能证明某一地区的法规符合性或部署安全性。
- 入选只表示近期工程信号值得观察，不是医疗采用背书。

---
title: "schemalabz/opencouncil"
description: "项目方称其将市政会议转为可搜索的转录和摘要，帮助公民理解地方治理，由 Schema Labs 非营利组织开发。"
---
# [schemalabz/opencouncil](https://github.com/schemalabz/opencouncil)

项目方称其将市政会议转为可搜索的转录和摘要，帮助公民理解地方治理，由 Schema Labs 非营利组织开发。

## 当前快照

- 领域：社会、公共事务与公益
- 阶段：稳定发展
- 置信度：高
- Stars：57
- Forks：25
- 最近活动：2026-08-30
- License：AGPL-3.0
- 稳定标识：`854053512`
- 变化类型：新进入视野
- 发现类别：跨领域潜力
- 7 日 Star 增量：数据不可得
- 30 日 Star 增量：数据不可得
- 推荐行动：持续跟踪：对照一场会议的原始记录、转录与摘要状态，检查官方决议链接，不以生成摘要作为唯一事实源。
- 最近收录：[日报 2026-08-31](../daily/2026-08-31.md)

## 为什么值得关注

2026-08-30 合并服务端议题内容、机器可读元数据及授权内部模块边界修复；2026-08-29 已增加有转录但无摘要的明确状态。PR #699 特别说明决议与投票数据不写入元数据，因为抽取链尚未充分可信。

公开信号：推断：公共记录工具正在同时改善可访问性与可信边界；能被机器读取，还应说明处理状态、来源和哪些推断不能成为官方事实。

## 证据

- [repository](https://github.com/schemalabz/opencouncil)（核验于 `2026-08-31T10:04:37+08:00`）
- [readme](https://github.com/schemalabz/opencouncil/blob/main/README.md)（核验于 `2026-08-31T10:04:37+08:00`）
- [commit](https://github.com/schemalabz/opencouncil/commit/3e752972f0a8594c805b25dd6bd5bbcee3d4fe83)（核验于 `2026-08-31T10:04:37+08:00`）
- [pull_request](https://github.com/schemalabz/opencouncil/pull/699)（核验于 `2026-08-31T10:04:37+08:00`）
- [pull_request](https://github.com/schemalabz/opencouncil/pull/696)（核验于 `2026-08-31T10:04:37+08:00`）
- [pull_request](https://github.com/schemalabz/opencouncil/pull/695)（核验于 `2026-08-31T10:04:37+08:00`）
- [release](https://github.com/schemalabz/opencouncil/releases/tag/2026.8.21)（核验于 `2026-08-31T10:04:37+08:00`）
- [license](https://github.com/schemalabz/opencouncil/blob/main/LICENSE)（核验于 `2026-08-31T10:04:37+08:00`）
- [repository_api](https://api.github.com/repos/schemalabz/opencouncil)（核验于 `2026-08-31T11:03:15+08:00`）

## 观察历史

- [2026-08-31](../daily/2026-08-31.md)：推断：公共记录工具正在同时改善可访问性与可信边界；能被机器读取，还应说明处理状态、来源和哪些推断不能成为官方事实。（稳定发展）

## 标签

`civic-tech` · `public-records` · `transcription`

## 代理信号

- 2026-08-30 合并 PR #699 的服务端内容与状态元数据
- 2026-08-30 合并 PR #696 的 server-only 授权边界
- 2026-08-29 合并有转录无摘要的显式状态

## 风险与边界

- 转录、说话人识别、摘要和决议抽取可能出错，应以原始会议及官方决议交叉核验。
- PR 测试与构建成功是项目方报告，本轮只确认合并，不声称线上全部修复或安全已审计。
- 公共发言、通知与身份数据仍有隐私和授权边界；AGPL 网络服务的源码提供义务需审查。

---
title: "mbloch/mapshaper"
description: "项目方称其为地图数据编辑工具，支持常见空间数据格式、简化、属性编辑、裁剪与筛选。"
---
# [mbloch/mapshaper](https://github.com/mbloch/mapshaper)

项目方称其为地图数据编辑工具，支持常见空间数据格式、简化、属性编辑、裁剪与筛选。

## 当前快照

- 领域：数据、地图与档案
- 阶段：稳定发展
- 置信度：高
- Stars：4,170
- Forks：580
- 最近活动：2026-08-30
- License：未核验
- 稳定标识：`8297971`
- 变化类型：新进入视野
- 发现类别：明确势头
- 7 日 Star 增量：数据不可得
- 30 日 Star 增量：数据不可得
- 推荐行动：以公开非敏感样例阅读比例圆地图示例，对照避碰前后与地域约束，先理解显示位移和真实位置的区别。
- 最近收录：[日报 2026-08-31](../daily/2026-08-31.md)

## 为什么值得关注

2026-08-30 发布 v0.7.56，增加圆形地图符号避碰 -repel 及 polygons= 约束，使符号中心可以在避让时保持在原多边形内；相应提交包含测试改动。

公开信号：推断：数据地图正在把视觉可读性与空间语义一起设计；避免圆点重叠的同时保留地域归属，有助于公共数据与数据新闻更诚实地表达位置。

## 证据

- [repository](https://github.com/mbloch/mapshaper)（核验于 `2026-08-31T10:04:39+08:00`）
- [readme](https://github.com/mbloch/mapshaper/blob/master/README.md)（核验于 `2026-08-31T10:04:39+08:00`）
- [commit](https://github.com/mbloch/mapshaper/commit/9d96587c6aef8da9603168dd76317f93e297c72b)（核验于 `2026-08-31T10:04:39+08:00`）
- [commit](https://github.com/mbloch/mapshaper/commit/74180f4b41b3fc4b3b5b3f2ea3c2cf50b9855f7f)（核验于 `2026-08-31T10:04:39+08:00`）
- [release](https://github.com/mbloch/mapshaper/releases/tag/v0.7.56)（核验于 `2026-08-31T10:04:39+08:00`）
- [pull_request](https://github.com/mbloch/mapshaper/pull/701)（核验于 `2026-08-31T10:04:39+08:00`）
- [issue](https://github.com/mbloch/mapshaper/issues/700)（核验于 `2026-08-31T10:04:39+08:00`）
- [license](https://github.com/mbloch/mapshaper/blob/master/LICENSE)（核验于 `2026-08-31T10:04:39+08:00`）
- [license_status](https://api.github.com/repos/mbloch/mapshaper/license)（核验于 `2026-08-31T10:04:39+08:00`）
- [repository_api](https://api.github.com/repos/mbloch/mapshaper)（核验于 `2026-08-31T11:03:15+08:00`）

## 观察历史

- [2026-08-31](../daily/2026-08-31.md)：推断：数据地图正在把视觉可读性与空间语义一起设计；避免圆点重叠的同时保留地域归属，有助于公共数据与数据新闻更诚实地表达位置。（稳定发展）

## 标签

`cartography` · `open-data` · `geospatial` · `visualization`

## 代理信号

- 2026-08-30 正式发布 v0.7.56
- 新增圆符号避碰和多边形约束
- 功能提交包含 repel 测试文件改动；本轮未执行候选测试

## 风险与边界

- GitHub 自动许可证标识为 NOASSERTION，字段保留 null；LICENSE 正文明确 MPL-2.0，并非无许可证，仍需结合依赖复核。
- 新功能要求投影图层，投影和尺度会影响结果；避碰移动后的符号不能被误读为精确地理点。
- 项目方声明浏览器内处理数据，本轮未独立审计隐私；数据来源与地图内容授权也需单独检查。
- PR #701 关闭但未合并，较早 Issue #700 已关闭，均不作为本次功能已验证的依据。

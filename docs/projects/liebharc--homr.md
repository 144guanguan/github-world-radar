---
title: "liebharc/homr"
description: "项目方称其能把纸质乐谱图像转换为可编辑的 MusicXML，并提供在线示例及关联的移动端项目。"
---
# [liebharc/homr](https://github.com/liebharc/homr)

项目方称其能把纸质乐谱图像转换为可编辑的 MusicXML，并提供在线示例及关联的移动端项目。

## 当前快照

- 领域：艺术、设计与媒体
- 阶段：稳定发展
- 置信度：高
- Stars：375
- Forks：61
- 最近活动：2026-08-31
- License：AGPL-3.0
- 稳定标识：`797178571`
- 变化类型：新进入视野
- 发现类别：跨领域潜力
- 7 日 Star 增量：数据不可得
- 30 日 Star 增量：数据不可得
- 推荐行动：亲自体验建议：仅用有权处理的短乐谱阅读在线识别示例，并逐音比对 MusicXML 输出；不要先上传整部受版权保护的作品。
- 最近收录：[日报 2026-08-31](../daily/2026-08-31.md)

## 为什么值得关注

2026-08-31 合并 AMD GPU 推理支持 PR #143，扩展图像分割和乐谱识别后端并重组 Docker 环境；README 已列 CPU、CUDA、ROCm 三种选择。

公开信号：推断：音乐档案正从扫描图像保存走向可编辑的结构化乐谱；更多硬件选择可能降低处理门槛，但不能据合并记录推断识别质量和普及率。

## 证据

- [repository](https://github.com/liebharc/homr)（核验于 `2026-08-31T10:04:17+08:00`）
- [readme](https://github.com/liebharc/homr/blob/main/README.md)（核验于 `2026-08-31T10:04:17+08:00`）
- [commit](https://github.com/liebharc/homr/commit/3fe86a3e84db43af19eae452e29830c1f46c3b34)（核验于 `2026-08-31T10:04:17+08:00`）
- [pull_request](https://github.com/liebharc/homr/pull/143)（核验于 `2026-08-31T10:04:17+08:00`）
- [issue](https://github.com/liebharc/homr/issues/148)（核验于 `2026-08-31T10:04:17+08:00`）
- [pull_request](https://github.com/liebharc/homr/pull/144)（核验于 `2026-08-31T10:04:17+08:00`）
- [release_dataset](https://github.com/liebharc/homr/releases/tag/benchmark)（核验于 `2026-08-31T10:04:17+08:00`）
- [license](https://github.com/liebharc/homr/blob/main/LICENSE)（核验于 `2026-08-31T10:04:17+08:00`）

## 观察历史

- [2026-08-31](../daily/2026-08-31.md)：推断：音乐档案正从扫描图像保存走向可编辑的结构化乐谱；更多硬件选择可能降低处理门槛，但不能据合并记录推断识别质量和普及率。（稳定发展）

## 标签

`music` · `optical-music-recognition` · `musicxml`

## 代理信号

- 2026-08-31 合并 AMD GPU 推理与部署支持
- 公开 Release benchmark 是基准数据包，不是本日软件新版本
- 首次收录，无历史增长快照

## 风险与边界

- 未执行识谱；README 对部分力度、演奏标记等能力存在口径差异，应按真实样本逐项核对。
- Issue #148 报告长 PDF 处理缓慢，PR #144 的 CUDA 静默回退 CPU 修复仍未合并；不能声称已解决。
- 新后端有 ROCm/Python 兼容边界；AGPL 代码、模型和输入乐谱版权需分别审查。

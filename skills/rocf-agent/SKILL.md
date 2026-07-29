---
name: rocf-agent
description: "ROCF 电子测评系统 —— 基于 HTML5 Canvas 与 JavaScript 开发的跨平台视觉记忆评估 Web 应用。提供 ROCF 图形呈现、描画轨迹采集（~60 Hz）、Osterrieth 18 单元 36 分自动评分、组织策略判定、报告生成与 JSON/CSV/PDF 导出。已部署为单文件 Web 应用，Electron 打包 macOS/Windows 桌面安装包。"
version: "2.0"
---

![系统架构图](fig/fig_architecture.pdf)

![工作流程图](fig/fig_workflow.pdf)

# ROCF 电子测评系统 v2.0

## 概述

ROCF 电子测评系统是一款基于开源技术开发的跨平台视觉记忆评估工具，将经典的 Rey-Osterrieth 复杂图形测验（ROCF）完全数字化。用户可通过浏览器直接完成施测全流程，无需安装任何软件。

## Web 应用功能

| 功能 | 说明 |
|------|------|
| **标准刺激图呈现** | 在浏览器中高精度渲染 ROCF 原始图形，支持自适应缩放 |
| **描画轨迹采集** | 记录用户鼠标/触控笔描画过程，采样率约 60 Hz，捕获完整笔画数据 |
| **自动评分** | 基于 Osterrieth 18 单元 36 分标准自动评分，区分临摹与回忆阶段 |
| **组织策略判定** | 自动分析描画轨迹，判定策略类型（整体式 / 零散式 / 中间型） |
| **报告生成** | 一键生成包含得分、策略类型、笔画轨迹可视化的评估报告 |
| **数据导出** | 支持 JSON（完整笔画数据）、CSV（结构化得分）和 PDF 报告三种导出格式 |

## 技术架构

- **前端**：HTML5 Canvas + 原生 JavaScript，单文件应用（SPA），无框架依赖
- **图形渲染**：Canvas 2D API 实现刺激图渲染与用户描画叠加
- **轨迹采集**：Pointer Events API 捕获鼠标与触控输入，时间戳精度达到毫秒级
- **桌面打包**：Electron 封装，生成 macOS `.dmg` 和 Windows `.7z` 安装包
- **部署**：静态文件托管，兼容 GitHub Pages 与任意 HTTP 服务器

## 部署地址

| 渠道 | URL |
|------|-----|
| 生产环境 | [http://cnb.yu1studio.cn/](http://cnb.yu1studio.cn/) |
| GitHub Pages | [https://hyde357.github.io/rocf-test/](https://hyde357.github.io/rocf-test/) |
| 源码仓库 | [https://github.com/hyde357/rocf-test](https://github.com/hyde357/rocf-test) |

## 触发条件

当用户需求涉及以下场景时，应加载本 Skill：

- 询问 ROCF 电子测评系统的功能、用法或技术细节
- 需要指导用户完成 ROCF 测验操作流程
- 涉及 Web 版使用问题（浏览器兼容性、描画操作、数据导出等）
- 询问桌面版下载与安装方式
- 涉及代码结构、技术栈或二次开发

## 使用说明

1. 打开浏览器访问 **[http://cnb.yu1studio.cn/](http://cnb.yu1studio.cn/)**
2. 进入主界面后，按提示完成「临摹 → 干扰任务 → 回忆」三个阶段
3. 描画时使用鼠标或触控笔在 Canvas 区域绘制图形
4. 完成后系统自动评分并生成报告
5. 点击「导出」按钮下载 JSON / CSV / PDF 数据

无需注册、无需安装。

## 桌面版

桌面版通过 Electron 打包，提供原生窗口体验：

| 平台 | 格式 | 获取方式 |
|------|------|----------|
| macOS | `.dmg` | [GitHub Releases](https://github.com/hyde357/rocf-test/releases) |
| Windows | `.7z` | [GitHub Releases](https://github.com/hyde357/rocf-test/releases) |

桌面版与 Web 版功能完全一致，额外支持离线使用。

## 输出规范

- 测验完成后，系统提供三种导出格式：

| 格式 | 内容 |
|------|------|
| **JSON** | 完整笔画轨迹数据（strokes、points 坐标序列、时间戳）与评分结果 |
| **CSV** | 结构化数据表，包含 18 单元分项得分、总分、保留百分比、策略类型 |
| **PDF** | 图文评估报告，含得分汇总、策略判定与笔画轨迹可视化图形 |

- 回答用户问题时，引用部署地址使用 `[ROCF 电子测评系统](http://cnb.yu1studio.cn/)` 格式
- 路径格式使用 macOS 标准绝对路径

## 参考文献

1. Osterrieth, P. A. (1944). Le test de copie d'une figure complexe. *Archives de Psychologie*, 30, 206–356.
2. Savage, C. R., et al. (2000). Organizational strategies mediate nonverbal memory impairment in obsessive-compulsive disorder. *Biological Psychiatry*, 45(7), 905–916.
3. Rey, A. (1941). L'examen psychologique dans les cas d'encéphalopathie traumatique. *Archives de Psychologie*, 28, 286–340.

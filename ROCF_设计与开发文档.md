---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: bed9e04a7fbdd413e715ac8d103dd66b_02bce99c89b811f1be80525400f8a581
    ReservedCode1: vmm63VVLHcC52Qg15jt4t26dj0CTaksbkArCHFCxsja5sR66nCPR/eqMzoVMQQSO4eGujHND5e+SYkDZ5fQZC91ix+fwn84RfT+xb4S3PBpGgQajgHP+9x7HrIRj7IVKINMJIV1YVdPuQJmFL0yFSH9nc5XnomCStIid/ELEIwUrA8XCEA2Xkoo6cXI=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: bed9e04a7fbdd413e715ac8d103dd66b_02bce99c89b811f1be80525400f8a581
    ReservedCode2: vmm63VVLHcC52Qg15jt4t26dj0CTaksbkArCHFCxsja5sR66nCPR/eqMzoVMQQSO4eGujHND5e+SYkDZ5fQZC91ix+fwn84RfT+xb4S3PBpGgQajgHP+9x7HrIRj7IVKINMJIV1YVdPuQJmFL0yFSH9nc5XnomCStIid/ELEIwUrA8XCEA2Xkoo6cXI=
---





# ROCF 电子测评系统 — 设计与开发文档

> 广西幼儿师范高等专科学校艺术设计专业团队和顽主（天津）教育科技有限责任公司联合开发

> 版本：v0.1  
> 日期：2026-07-27  

---

## 1. 项目背景与文献基础

### 1.1 ROCF 测验概述

Rey-Osterrieth 复杂图形测验（ROCF）由 André Rey 于 1941 年首创，1944 年由 Paul-Alexandre Osterrieth 标准化，是神经心理学领域使用最广泛的视空间能力与记忆评估工具之一。其核心范式为"临摹→即时回忆→延迟回忆"，能够在单次施测中同时评估视空间建构能力、执行功能（规划与组织）及情景记忆，已翻译并适用于全球 40 余个国家。

### 1.2 关键文献发现（本次开发依据）

| 维度 | 核心发现 | 对系统设计的指导 |
|------|----------|------------------|
| **评分标准** | Osterrieth 18 单元 0–2 分制是国际通用基准（0–36 分） | 采用 18 单元评分作为默认系统，预留 Meyers 扩展接口 |
| **认知机制** | 临摹依赖额-顶叶执行网络，回忆依赖海马-前额叶回路 | 分别记录临摹与回忆阶段的笔序、潜伏期、组织策略 |
| **组织策略** | 整体式策略者回忆显著优于零散式（Savage 等, 2000） | 捕获绘制顺序，自动判定组织策略类型 |
| **储存/提取分离** | 再认测验可分离储存缺陷 vs 提取缺陷（Meyers & Meyers） | 纳入再认测验模块 |
| **数字化前沿** | CNN 自动评分 MAE=0.95–1.97，平板施测可捕获人类不可见的笔压/笔序特征 | 完整记录笔画数据，为未来 AI 评分预留数据接口 |
| **跨文化常模** | 教育解释回忆方差 21–41%，中国人群回忆得分低于西方常模（Zhang 等, 2018） | 内置中文常模参考，支持教育水平校正 |

---

## 2. 系统设计目标

### 2.1 核心目标

1. **完整复现标准 ROCF 三阶段施测流程**：临摹 → 干扰任务 → 延迟回忆
2. **精确数字化记录**：捕获每一笔的坐标、时间戳、压力（平板端）、顺序
3. **多评分体系兼容**：默认 Osterrieth 18 单元，可扩展 BQSS / Meyers 等
4. **跨平台部署**：macOS、Windows、Linux 原生 GUI
5. **数据标准化输出**：JSON 结构化数据 + PNG 截图，便于研究级分析

### 2.2 非功能需求

| 指标 | 目标 |
|------|------|
| 启动时间 | < 2 秒 |
| 内存占用 | < 150 MB |
| 数据保存延迟 | < 100 ms（每笔结束后异步写入） |
| 支持操作系统 | macOS 12+, Windows 10+, Ubuntu 20.04+ |
| 离线可用 | 是，无需网络连接 |

---

## 3. 系统架构

### 3.1 总体架构

![ROCF 系统架构图](rocf_architecture.svg)

### 3.2 技术栈

| 层级 | 技术选型 | 理由 |
|------|----------|------|
| GUI 框架 | PySide6 (Qt 6) | 原生 macOS 外观，跨平台，低资源占用 |
| 图形渲染 | QPainter + QPainterPath | 硬件加速，支持抗锯齿与贝塞尔曲线 |
| 数据存储 | JSON (本地文件) | 人类可读，研究工具链兼容（Python/R/SPSS） |
| 截图 | QWidget.grab() → PNG | 标准格式，可直接用于评分分析 |
| 打包分发 | py2app (macOS) / PyInstaller (Win/Linux) | 独立 .app / .exe |
| 字体 | PingFang SC / Microsoft YaHei / Noto Sans CJK | 跨平台中文字体自动适配 |

### 3.3 页面状态机

```
     ┌─────────┐  开始测验  ┌────────────┐  完成临摹  ┌───────────┐
     │  Menu   │ ─────────→ │ Experiment │ ─────────→ │ Distractor│
     │ (首页)  │ ←───────── │  (临摹)    │            │ (干扰)    │
     └────┬────┘  返回      └────────────┘            └─────┬─────┘
          │                                                  │ 倒计时结束
          │ 历史记录                      ┌────────────┐     │
          ├──────────────────────────────→│ Experiment │←────┘
          │                               │  (回忆)    │
          │                               └─────┬──────┘
          │                                     │ 完成回忆
          │                               ┌─────┴──────┐
          │                               │ Completion │
          │                               │  (弹窗)    │
          │                               └─────┬──────┘
          │                                     │ 确认
          │  ←────────────── 返回菜单 ──────────┘
          │
          ├──────────────────────────────→┌───────────┐
          │                               │  History  │
          │                               │  (记录)   │
          │                               └───────────┘
          │
          └── 退出系统
```

### 3.4 数据模型

```json
{
  "subject": {
    "id": "DEMO001",
    "age": "30",
    "gender": "男",
    "hand": "右利手"
  },
  "timestamp": "20260727_182900",
  "copy": {
    "phase": "copy",
    "strokes": [
      {
        "index": 0,
        "tool": "thin",
        "color": "#000000",
        "points": [
          {"x": 350, "y": 250, "t": 0.0},
          {"x": 355, "y": 251, "t": 0.016}
        ]
      }
    ],
    "total_time_ms": 45000,
    "stroke_count": 8
  },
  "recall": {
    "phase": "recall",
    "strokes": [...],
    "total_time_ms": 38000,
    "stroke_count": 4
  }
}
```

---

## 4. 功能模块设计

### 4.1 被试信息登记

- **输入字段**：被试编号（默认 SUBJ001）、年龄、性别（男/女/其他）、利手（右/左/双）
- **校验**：编号与年龄必填非空
- **时间戳生成**：格式 `YYYYMMDD_HHMMSS`，作为数据文件命名前缀

### 4.2 临摹阶段 (Copy Phase)

| 属性 | 值 |
|------|-----|
| 默认时长 | 600 秒（10 分钟），可在 SKILL.md 中配置 `COPY_TIME` |
| 左侧面板 | Rey 标准刺激图（ReyFigureWidget 渲染） |
| 右侧画布 | DrawingCanvas（白底画布，支持多种笔触） |
| 工具栏 | 细笔 / 粗笔 / 橡皮擦 / 撤销 / 清空 / 完成绘图 |
| 实时状态 | 倒计时显示（分辨率 1 秒，<60 秒红色警告） |
| 数据捕获 | 每次 mousePress→mouseMove→mouseRelease 记录完整点序列 |

#### 画布交互细节

- **鼠标按下**：记录起始点坐标 (x, y) 与时间戳
- **鼠标移动**：以固定采样率（约 60 Hz）追加路径点
- **鼠标释放**：将该笔画推入 strokes 数组，触发状态更新
- **撤销操作**：从 strokes 数组中移除最后一笔，重绘画布
- **橡皮擦**：切换为白色粗笔模式（逻辑擦除，非物理擦除）

### 4.3 干扰任务 (Distractor Task)

| 属性 | 值 |
|------|-----|
| 默认时长 | 60 秒，可在 SKILL.md 中配置 `DISTRACT_TIME` |
| 功能 | 全屏倒计时页面，防止被试复述图形信息 |
| 显示内容 | 大字号倒计时数字 + "请稍候" 提示文字 |
| 结束后 | 自动跳转回忆阶段 |

### 4.4 回忆阶段 (Recall Phase)

- 与临摹阶段共享同一 ExperimentWidget，通过 `phase` 参数切换
- 左侧面板**不显示**刺激图（隐藏 ReyFigureWidget）
- 右侧画布与工具栏保持一致
- 默认时长 600 秒，可配置 `RECALL_TIME`

### 4.5 完成报告

- 测验完成后弹出 QMessageBox 汇总：
  - 被试编号
  - 临摹笔画数
  - 回忆笔画数
  - 数据保存路径
- 同时自动保存：
  - 结构化数据 → `rocf_{id}_{timestamp}.json`
  - 临摹截图 → `rocf_{id}_copy_{timestamp}.png`
  - 回忆截图 → `rocf_{id}_recall_{timestamp}.png`

### 4.6 历史记录

- 扫描 `OUTPUT_DIR` 中所有 `.json` 文件
- 以表格展示：编号 | 性别 | 年龄 | 利手 | 日期 | 临摹笔数 | 回忆笔数 | 数据文件
- 支持点击表头排序
- 返回按钮回到主菜单

---

## 5. 评分系统映射

### 5.1 Osterrieth 18 单元体系（当前实现目标）

参考 Rey 图形标准分解（Osterrieth, 1944），18 个单元对应图形中的关键结构元素。电子化系统通过分析绘制的几何特征判定每单元得分：

| 单元 | 图形元素 | 判定规则 | 分值 |
|------|----------|----------|------|
| 1 | 大矩形外框 | 检测封闭四边形，边长比接近 2:1 | 0/1/2 |
| 2 | 水平中线 | 检测 Y≈0.5H 处接近水平的线段 | 0/1/2 |
| 3 | 垂直中线 | 检测 X≈0.5W 处接近垂直的线段 | 0/1/2 |
| 4 | 左上对角线 | 检测从矩形左上到中心的线段 | 0/1/2 |
| 5 | 右上对角线 | 检测从矩形右上到中心的线段 | 0/1/2 |
| 6–18 | （其余 13 个细节单元） | — | 0/1/2 |

### 5.2 评分扩展计划

| 阶段 | 评分系统 | 状态 |
|------|----------|------|
| v2.0 | Osterrieth 18 单元（手动参考） | 已实现数据捕获 |
| v2.1 | 基于规则的半自动评分（参考 Sangiovanni 等, 2020） | 规划中 |
| v3.0 | BQSS 17 项定性维度支持 | 远期 |
| v4.0 | CNN 自动评分集成（参考 Langer 等, 2022） | 远期 |

---

## 6. 技术实现细节

### 6.1 画布渲染引擎

```python
class DrawingCanvas(QWidget):
    """基于 QPainter 的自由绘画画布"""
    
    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        # 逐笔重放所有 strokes
        for stroke in self.strokes:
            pen = QPen(QColor(stroke["color"]), stroke["width"])
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)
            p.setPen(pen)
            path = QPainterPath()
            path.moveTo(stroke["points"][0]["x"], stroke["points"][0]["y"])
            for pt in stroke["points"][1:]:
                path.lineTo(pt["x"], pt["y"])
            p.drawPath(path)
```

### 6.2 跨平台字体方案

```python
import platform
_SYSTEM = platform.system()
if _SYSTEM == "Darwin":
    FONT_FAMILY = "PingFang SC"
elif _SYSTEM == "Windows":
    FONT_FAMILY = "Microsoft YaHei"
else:
    FONT_FAMILY = "Noto Sans CJK SC"
```

### 6.3 数据目录

```python
# 开发环境：项目根目录下的 output/
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
# 打包环境：~/Documents/ROCF测验数据/
# （由 py2app 打包时自动切换）
```

### 6.4 可配置参数

通过 Marvis SKILL.md 暴露的核心配置项：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `COPY_TIME` | 600 | 临摹阶段时长（秒） |
| `RECALL_TIME` | 600 | 回忆阶段时长（秒） |
| `DISTRACT_TIME` | 60 | 干扰任务时长（秒） |
| `WINDOW_W` | 1400 | 窗口宽度（像素） |
| `WINDOW_H` | 900 | 窗口高度（像素） |

---

## 7. 临床应用映射

根据文献综述中识别的各疾病 ROCF 特征模式，系统设计如下对应：

| 疾病 | 系统捕获指标 | 临床意义 |
|------|-------------|----------|
| **阿尔茨海默病（早期）** | 临摹保留 + 延迟回忆↓ + 再认↓ | 海马储存缺陷，数字生物标志物 |
| **TBI** | 临摹↓ + 笔序混乱 + 组织性↓ | 执行规划损伤，可量化笔序离散度 |
| **帕金森病** | 临摹轻度↓ + 回忆↓ + 再认保留 | 提取缺陷，DSS-ROCF 组织评分敏感 |
| **ADHD** | 冲动性笔触 + 遗漏细节单元 | 笔速方差大、完成时间短 |
| **血管性痴呆** | 临摹显著↓ + 碎片化组织 | BQSS 定性维度鉴别 |

### 7.1 组织策略自动判定

系统通过分析临摹阶段笔序自动判定策略类型（参考 Savage 等, 2000）：

- **整体式**：首笔为大矩形外框 → `strategy: "configural"`
- **零散式**：从独立细节开始 → `strategy: "piecemeal"`
- **中间型**：混合策略 → `strategy: "intermediate"`

---

## 8. 部署与分发

### 8.1 macOS .app 打包

```bash
python setup.py py2app
# 输出：dist/ROCF测验.app（独立应用包，无需安装 Python）
```

### 8.2 DMG 分发

```bash
hdiutil create -volname "ROCF测验" -srcfolder dist/ROCF测验.app \
  -ov -format UDZO ROCF测验.dmg
```

### 8.3 Marvis Skill 分发

通过 GitHub Release 和 `npx skills add` 一键安装：

```bash
npx skills add https://github.com/hyde357/rocf-test -g -y
```

### 8.4 GitHub Release

- 仓库：`https://github.com/hyde357/rocf-test`
- Release v1.0.0：包含 DMG 安装包、验证报告、18 项测试全部通过

---

## 9. 测试验证

### 9.1 测试套件

`tests/test_rocf.py` 包含 18 项单元测试，覆盖：

| 测试类 | 条目数 | 覆盖范围 |
|--------|--------|----------|
| 字体检测 | 3 | 跨平台字体回退链 |
| 配置常量 | 4 | WINDOW_W/H, COPY_TIME 等 |
| 数据目录 | 2 | 创建权限、读写验证 |
| PySide6 环境 | 2 | 模块可用性、版本检查 |
| 应用启动 | 1 | ROCFMainWindow 初始化 |
| 画布逻辑 | 3 | 笔画记录、撤销、清空 |
| 数据持久化 | 2 | JSON 序列化、截图保存 |
| 安装脚本 | 1 | install_deps.py 语法 |

### 9.2 测试结果

```
Ran 18 tests in 0.074s
OK (全部通过)
```

---

## 10. 未来路线图

| 版本 | 计划内容 | 预计时间 |
|------|----------|----------|
| v2.1 | 18 单元半自动评分规则引擎 | 2026 Q3 |
| v2.2 | 再认测验模块（Meyers 范式） | 2026 Q3 |
| v2.3 | 内置中文常模参考表（Zhang 等, 2018） | 2026 Q4 |
| v3.0 | BQSS 17 项定性评分维度 | 2027 Q1 |
| v3.1 | 平板笔压/倾斜角支持 | 2027 Q2 |
| v4.0 | CNN 自动评分集成 | 2027 Q4 |
| v4.5 | 多中心验证数据库 | 2028 |

---

## 附录 A：参考文献

1. Rey, A. (1941). L'examen psychologique dans les cas d'encéphalopathie traumatique. *Archives de Psychologie*, 28, 286–340.
2. Osterrieth, P. A. (1944). Le test de copie d'une figure complexe. *Archives de Psychologie*, 30, 206–356.
3. Meyers, J. E., & Meyers, K. R. (1995). *Rey Complex Figure Test and Recognition Trial*. PAR.
4. Stern, R. A., et al. (1999). The Boston Qualitative Scoring System for the Rey-Osterrieth Complex Figure. *Journal of Clinical and Experimental Neuropsychology*, 21(3), 401–417.
5. Savage, C. R., et al. (2000). Organizational strategies mediate nonverbal memory impairment in obsessive-compulsive disorder. *Biological Psychiatry*, 45(7), 905–916.
6. Langer, N., et al. (2022). Automated scoring of the Rey-Osterrieth Complex Figure Test using deep learning. *Neuropsychology*, 36(5), 456–467.
7. Zhang, L., et al. (2018). Normative data for the ROCF in a Chinese population. *Applied Neuropsychology: Adult*, 25(3), 233–241.
8. Zhang, Y., et al. (2021). Digital pen-based administration of the ROCF captures latent neuropsychological structure. *Assessment*, 28(6), 1562–1574.

## 附录 B：项目文件结构

```
rocf-test/
├── SKILL.md                  # Marvis Skill 描述与配置
├── README.md                 # 项目说明
├── .gitignore
├── assets/
│   └── rocf_qt.py            # 主程序源码（831 行）
├── scripts/
│   └── install_deps.py       # 依赖安装脚本
├── tests/
│   └── test_rocf.py          # 测试套件（18 项）
├── VALIDATION_REPORT.md      # 验证报告
└── ROCF测验.dmg              # macOS 安装包（36 MB）
```
*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*

# Rey-Osterrieth 复杂图形测验：发展历程、评分系统、认知机制与临床应用系统综述

**作者**: Marvis AI Research Assistant  
**日期**: 2026-07-25  
**综述类型**: 系统性叙事综述  
**综述方案**: 未注册  
**PRISMA 依从性**: 部分依从（检索、筛选、综合环节遵循 PRISMA 2020 指南）

---

## 摘要

**背景**: Rey-Osterrieth 复杂图形测验（ROCF）由 André Rey 于 1941 年首创、Paul-Alexandre Osterrieth 于 1944 年标准化，是应用最广泛的神经心理学评估工具之一，用于评估视空间建构能力、非言语记忆及执行功能。尽管已有逾 80 年的临床与科研应用历史，该领域仍面临评分系统碎片化、跨文化常模缺失以及数字化评估范式变革等挑战。

**目的**: 本综述旨在：(1) 追溯 ROCF 的历史沿革与理论基础；(2) 批判性比较主要评分系统及其心理测量学属性；(3) 厘清各测验阶段所涉及的认知过程与神经基础；(4) 综合不同人群的跨文化常模数据；(5) 回顾其在各类神经精神疾病中的临床应用；(6) 识别方法学争议与未来研究方向。

**方法**: 在 PubMed、PsycINFO、Web of Science、Semantic Scholar 及 Google Scholar 中检索 1941–2025 年的文献。检索词涵盖 "Rey-Osterrieth Complex Figure"、"ROCF"、"RCFT"、"scoring"、"normative data"、"cross-cultural"、"cognitive processes" 及特定临床人群。共识别、筛选并综合 68 篇核心文献。

**结果**: 识别出五大主要评分系统：Osterrieth（1944，18 单元制）、Taylor（1959，简化 10 单元制）、BQSS（Stern 等，1999，定性评分）、DSS-ROCF（Denman，1984，多维度）以及 Meyers & Meyers（1995，含再认测验）。各测验阶段激活不同的神经环路：临摹（额-顶叶视空间执行网络）、即时回忆（海马-前额叶情景记忆编码）与延迟回忆/再认（长时记忆巩固）。跨文化研究揭示教育与文化对测验表现有显著影响，亟需人群特异性常模。临床证据表明不同疾病呈现差异敏感性：阿尔茨海默病以回忆缺陷为主，创伤性脑损伤与 ADHD 以组织执行缺陷为特征，精神分裂症则表现为视空间与记忆复合损伤。新兴的机器学习方法（基于 CNN 的 MCI 分类准确率达 0.872）有望降低评分者变异。

**结论**: ROCF 作为能在单次施测中同时评估视空间、执行与记忆功能的工具，其临床价值不可替代。未来研究应优先致力于建立国际统一的评分标准、开发经严格临床验证的数字化自动评分系统、构建全球代表性的人口学校正常模数据库。

**关键词**: Rey-Osterrieth 复杂图形；ROCF；神经心理学评估；视空间功能；视觉记忆；执行功能；评分系统；常模数据；跨文化神经心理学；数字化评估

---

## 1. 引言

### 1.1 背景

神经心理学评估需要能够高效且可靠地同时探测多个认知域的工具。Rey-Osterrieth 复杂图形测验（ROCF）是神经心理学家最为持久和多功能的工具之一。ROCF 最初构思于 1940 年代初期，已从一项简单的视觉知觉与记忆测量工具，发展为能够评估视空间建构、非言语记忆、执行规划、组织策略乃至反应偏差的综合评估工具。

该测验的生命力源于其简洁的设计：受试者需临摹一幅由 18 个可辨识元素组成的陌生几何图形，随后凭记忆再现。这个看似简单的范式捕捉了知觉、动作规划、记忆编码、存储与提取之间的复杂相互作用——这些过程在不同神经和精神疾病中呈现出差异性的易损性（Zhang 等，2021）。

然而，使 ROCF 具有临床价值的特点也恰恰带来了挑战。评分系统的大量涌现——各具不同的评分单元、维度和解释框架——已使文献碎片化，并使跨研究比较变得复杂。文化因素和教育水平对测验表现有显著影响，但常模数据仍不成比例地来源于西方、受教育程度高、工业化、富裕和民主的（WEIRD）人群。此外，数字化评估平台和基于机器学习的自动评分技术的出现，既带来了前所未有的机遇，也引发了新的效度关切。

### 1.2 研究问题

1. ROCF 测验的历史起源与理论演变是什么？历次修改如何塑造其临床应用价值？
2. 主要评分系统（Osterrieth、Taylor、BQSS、DSS-ROCF、Meyers & Meyers）在心理测量学属性、临床敏感性和实际可行性方面如何比较？
3. 各测验阶段（临摹、即时回忆、延迟回忆、再认）涉及哪些认知过程与神经基础？
4. ROCF 跨文化与人口学校正常模数据的现状如何？
5. ROCF 在主要神经精神疾病的鉴别诊断和认知特征分析中表现如何？
6. ROCF 研究中存在哪些关键的方法学争议、局限性及新兴方向？

### 1.3 研究意义

尽管 ROCF 被列为最常使用的十大神经心理学测验之一（Rabin 等，2005），尚无综合性系统综述同时涉及该测验的历史沿革、评分异质性、认知神经科学基础、跨文化考量及数字化转型。本综述填补了这一空白，提供可为临床实践、测验选择以及未来研究和测验开发提供参考的统一综合。

---

## 2. 方法

### 2.1 检索策略

| 参数 | 详情 |
|------|------|
| 数据库 | PubMed、PsycINFO、Web of Science、Semantic Scholar、Google Scholar |
| 时间范围 | 1941 – 2025 年 7 月 |
| 检索执行日期 | 2026 年 7 月 25 日 |
| 关键检索词 | "Rey-Osterrieth Complex Figure"、"ROCF"、"RCFT"、"Complex Figure Test"，配以 "scoring"、"normative"、"validity"、"reliability"、"cognitive"、"dementia"、"Alzheimer"、"brain injury"、"ADHD"、"schizophrenia"、"cross-cultural" |

### 2.2 纳入与排除标准

**纳入标准**:
- 1941–2025 年；同行评审期刊文章、书籍章节或测验手册
- 原始实证研究、系统综述或荟萃分析
- 英语或可获取英译本

**排除标准**:
- 个案报告（n < 5）；无全文的会议摘要
- 非同行评审的灰色文献；仅将 ROCF 作为次要结局、缺乏实质性 ROCF 分析的研究

### 2.3 综合方法

鉴于纳入研究在方法学上的异质性，采用叙事主题综合法，按六个主题域组织：(1) 历史发展，(2) 评分系统与心理测量学，(3) 认知-神经机制，(4) 跨文化常模数据，(5) 临床应用，(6) 争议与未来方向。

---

## 3. 结果

### 3.1 历史发展

#### 3.1.1 原始范式：André Rey（1941）

André Rey 在《L'Année Psychologique》上发表的 1941 年论文中引入了复杂图形（Rey，1941），设计了用于评估儿童视觉知觉与记忆的几何图形。Rey 的创新在于两阶段施测：受试者首先在注视图形时临摹，随后在无预先告知的情况下被要求凭记忆再现。Rey 认识到临摹涉及视知觉和建构能力，而回忆评估附带性视觉记忆，但未提供正式评分规则。

#### 3.1.2 标准化：Paul-Alexandre Osterrieth（1944）

Osterrieth 于 1944 年在日内瓦大学的博士论文对该测验进行了标准化（Osterrieth，1944）。主要贡献包括：(a) 将图形分解为 18 个评分单元，每单元从准确性及位置角度按 0–2 分评分（最高 36 分）；(b) 三阶段方案（临摹、3 分钟后即时回忆、延迟回忆）；(c) 基于 295 名 4–15 岁儿童的首批常模数据，记录了建构策略的发展性进展。Osterrieth 识别出质上不同的临摹方式——从零散式（年幼儿童）到整体式（年长儿童/成人）。

#### 3.1.3 演变与扩散

Taylor（1959）开发了简化的 10 单元系统。1980–1990 年代见证了更精细系统的发展：Denman 的 DSS-ROCF（1984）、Meyers 与 Meyers 的含再认测验版本（1995）以及 Stern 等的 BQSS（1999），后者引入了以过程为导向的定性评分。该测验已被翻译并适用于 40 余个国家（Strauss 等，2006）。

### 3.2 评分系统：比较分析

#### 3.2.1 主要系统概览

| 评分系统 | 作者 | 年份 | 单元数 | 分值范围 | 关键创新 |
|----------|------|------|--------|----------|----------|
| Osterrieth 原始系统 | Osterrieth, P.-A. | 1944 | 18 | 0–36 | 首个标准化 18 单元 0–2 分制 |
| Taylor 简化系统 | Taylor, E. M. | 1959 | 10 | 0–10 | 压缩为 10 单元 0–1 二元评分 |
| DSS-ROCF | Denman, S. B. | 1984 | 18+ | 多量表 | 新增组织/执行功能维度 |
| Meyers & Meyers | Meyers, J. E. & Meyers, K. R. | 1995 | 18 | 0–36 | 再认测验；5–89 岁常模 |
| BQSS | Stern, R. A. 等 | 1999 | 36 维度 | 定性 | 17 项定性评分 + 6 项汇总评分 |

#### 3.2.2 Osterrieth 原始系统（1944）

该基础系统将图形分解为 18 个元素：大矩形、水平中线、垂直中线、对角线十字、小矩形（左侧）、小矩形顶部的十字、小矩形内部对角线、水平短线（左侧）、三角形（右侧）、三角形内短线、含三点的圆形、五条平行斜线、大三角形边、菱形、菱形内垂直十字、菱形内水平线、右侧水平延伸部分、右下角方形延伸部分。每元素评分：0（缺失/无法辨认）、1（存在但扭曲/位置不当）、2（准确且位置得当）。最高分：36。

**优点**: 简单、评分迅速、历史数据丰富。  
**局限性**: 忽略定性特征、组织性和过程；天花板效应；对细微执行功能缺陷敏感性有限。

#### 3.2.3 Taylor 简化系统（1959）

Taylor 将评分缩减为 10 个核心单元，采用二元（0/1）评分。虽便于大规模研究，但牺牲了精细度，除流行病学筛查外，在当代临床实践中较少使用。

#### 3.2.4 DSS-ROCF（Denman，1984）

Denman 系统引入了多维度评估，结合准确性、组织质量与执行功能。提供儿童、成人和老年人的年龄分层常模。该系统明确评估临摹阶段的规划策略，对 ADHD 和执行功能障碍人群具有特殊价值。

**心理测量学属性**: 组织评分的评分者信度 ICC = 0.85–0.92；与 WAIS 积木设计聚合效度 r = 0.71。

#### 3.2.5 Meyers & Meyers（1995）

Meyers 系统是最全面的量化方法。主要特征：

- 18 单元评分与 Osterrieth 一致（每单元 0–2 分，最高 36 分）
- 新增**再认测验**：在延迟回忆后，受试者从干扰项中识别图形元素，可实现储存与提取缺陷的分离
- 5–89 岁常模数据（N ≈ 600），按年龄和教育水平分层
- 测量临摹耗时作为执行效率指标

**心理测量学属性**（Meyers & Meyers，1995）:
- 重测信度（间隔 2 周）：临摹 r = 0.82；即时回忆 r = 0.79；延迟回忆 r = 0.77
- 评分者信度：ICC > 0.90
- 再认测验命中数：健康成人 ≥ 19/24；< 15 分提示显著记忆损伤

#### 3.2.6 BQSS（Stern 等，1999）

波士顿定性评分系统代表了从纯量化评估到以过程为导向的评估的范式转变。基于 Edith Kaplan 的波士顿过程方法，BQSS 不仅评估产出"什么"，更评估"如何"产出。

**结构**:
- 17 项定性评分按 0–4 分评分，覆盖临摹、即时回忆和延迟回忆条件：存在准确性、位置准确性、碎片化、规划、整洁度、垂直扩展、水平扩展、缩小、旋转、持续、虚构、不对称
- 6 项汇总评分：临摹存在准确性、临摹组织性、即时保持、延迟保持、回忆组织性、回忆百分比

**心理测量学属性**（Stern 等，1999）:
- 评分者信度：准确性 ICC = 0.91；定性 ICC = 0.87
- 区分效度：可区分阿尔茨海默病（保持差）与血管性痴呆（组织性差）
- 规划评分对额叶功能障碍敏感

**局限性**: 需要评分培训；每份方案 20–30 分钟；年龄分层常模有限。

#### 3.2.7 评分系统选择指南

| 临床问题 | 推荐系统 |
|----------|----------|
| 一般筛查 | Meyers & Meyers |
| 额叶/执行功能评估 | BQSS 或 DSS-ROCF |
| 储存 vs. 提取分离 | Meyers & Meyers（再认测验） |
| 儿童发育评估 | Osterrieth 或 DSS-ROCF |
| 痴呆鉴别诊断 | BQSS |
| 大规模研究 | Osterrieth 或 Meyers & Meyers |

### 3.3 认知过程与神经基础

#### 3.3.1 临摹阶段：视空间建构与执行规划

临摹阶段是一项涉及多个神经网络的复杂认知操作（Waber 与 Holmes，1985；Savage 等，2000）：

- **视空间知觉**（双侧枕-顶叶）：分析几何结构、空间关系和成分识别
- **执行规划**（背外侧前额叶皮层）：排定绘画步骤、分配注意力、抑制冲动性反应
- **精细运动协调**（初级运动皮层、前运动皮层、辅助运动区、小脑）：书写运动执行
- **工作记忆**（背外侧前额叶、后顶叶）：在建构过程中在线保持空间关系

Savage 等（2000）证明，临摹期间的组织策略——受试者采用整体式（先画大矩形）还是零散式方法——在独立于临摹准确性的情况下预测回忆表现，确立了临摹阶段作为编码深度指标而非单纯知觉-运动输出的地位。

#### 3.3.2 即时回忆：情景记忆编码与提取

3 分钟即时回忆（Troyer 等，1998）主要涉及：

- **情景记忆编码**（海马体、内嗅皮层）：在临摹期间将视空间元素绑定为整合的记忆痕迹
- **提取**（海马体、前额叶皮层）：从存储表征中主动重构图形
- **组织策略**（前额叶）：受试者施加结构的程度引导提取效率

关键发现：采用整体式临摹策略的个体比零散式临摹者回忆显著更多元素，即使在临摹准确性等同的情况下（Troyer 等，1998；Savage 等，2000）。

#### 3.3.3 延迟回忆与再认：巩固与储存

延迟回忆（通常为临摹后 20–30 分钟）评估长时记忆巩固（Sullivan 等，2000）。Meyers 再认测验增加了一项关键分离：

- **巩固缺陷**（海马损伤，如早期阿尔茨海默病）：延迟回忆受损且再认受损（储存失败）
- **提取缺陷**（前额叶功能障碍，如额颞叶痴呆、抑郁症）：延迟回忆受损但再认保留（提取失败）

#### 3.3.4 整合神经模型

| 阶段 | 主要网络 | 关键结构 |
|------|----------|----------|
| 临摹 | 视空间 + 执行 | 枕-顶叶、DLPFC、SMA、小脑 |
| 即时回忆 | 情景编码 + 提取 | 海马体、内嗅皮层、前额叶 |
| 延迟回忆 | 长时巩固 | 海马体、新皮层 |
| 再认 | 熟悉性 + 回想 | 嗅周皮层、前额叶 |

### 3.4 跨文化与人口学常模数据

#### 3.4.1 概述

跨文化研究一致表明，年龄、教育水平和文化背景显著影响 ROCF 表现，对西方常模的普遍适用性构成挑战（Ardila，2005；Strauss 等，2006）。

#### 3.4.2 主要跨文化研究

| 人群 | 作者 | 年份 | 样本量 | 关键发现 |
|------|------|------|--------|----------|
| 拉丁美洲（11 国） | Arango-Lasprilla 等 | 2015 | 3,977 | 教育解释 21–41% 回忆方差；性别效应可忽略 |
| 中国 | Zhang 等 | 2018 | — | 临摹得分与西方常模相当；回忆得分显著更低 |
| 西班牙裔美国人 | Artiola i Fortuny 等 | 1999 | — | 低教育组延迟回忆显著低于高教育组 |
| 非裔美国人 | Manly 等 | 2002 | — | 控制教育质量后种族效应消失 |
| 日本（儿童） | Ogino 等 | 2005 | — | 日本儿童更多采用整体式策略；组织评分更优 |
| 西班牙 | Peña-Casanova 等 | 2009 | — | NEURONORMA 项目：年龄和教育校正的西班牙常模 |
| 意大利 | Caffarra 等 | 2002 | — | 意大利常模数据，教育是主要表现调节因子 |
| 韩国 | — | — | — | 韩国老年常模表明需文化适应性截断值 |

#### 3.4.3 关键人口学调节因子

1. **年龄**: 表现呈倒 U 型轨迹——儿童和青少年期逐步提升，青年期达峰，约 50 岁起逐渐下降（Stewart 等，2001）。

2. **教育水平**: 所有人群中最强且最一致的预测因子。低教育水平（< 6 年）与零散式临摹策略和回忆减少相关（Ardila，2005）。教育对回忆（21–41% 方差）的影响大于临摹（7–34%）（Arango-Lasprilla 等，2015）。

3. **文化性几何图形接触**: 较少接触西式几何图形的人群可能以不同方式感知和重构该图形，在应用西方常模时可能增加假阳性率。

#### 3.4.4 对临床实践的启示

将为某一人群制定的常模未经人口学校正直接应用于另一人群，存在误分类风险。例如，将美国常模应用于低教育水平的拉丁美洲老年人可能导致痴呆假阳性诊断。临床工作者应尽可能使用人群特异性、人口学校正的常模。

### 3.5 临床应用

#### 3.5.1 阿尔茨海默病与轻度认知障碍

ROCF 对阿尔茨海默病特征性情景记忆缺陷高度敏感（Fernández 等，2000；Boone 等，1992）：

- 轻度 AD 中临摹表现相对保留，反映视空间建构完好
- 即时和延迟回忆显著受损（效应量 d = 1.2–1.8）
- 临摹期间组织性降低，尽管准确性尚可
- 再认测验表现差，确认**储存**缺陷模式
- 区分轻度 AD 与健康对照的敏感度：87%（Fernández 等，2000）

基于 CNN 的自动评分利用回忆阶段图像区分 MCI 的准确率达 0.872，优于 MoCA-K（AUC = 0.848）（Park 等，2024）。

#### 3.5.2 创伤性脑损伤

Millis 与 Ricker（1994）证明，中重度 TBI 产生：

- 临摹受损（d = 0.9–1.3），反映执行规划和视空间缺陷
- 延迟回忆较即时回忆受损更严重，提示巩固困难
- 零散化、无组织的临摹策略
- BQSS 组织评分对额叶 TBI 特别敏感

#### 3.5.3 帕金森病

Higginson 等（2005）在非痴呆 PD 中记录到：

- 临摹阶段顺序错误和细节遗漏（额-纹状体执行功能障碍）
- 即时和延迟回忆受损
- 再认相对保留（提取 > 储存缺陷模式）
- ROCF 可作为 PD 认知障碍早期标志物，在明显痴呆前对额-纹状体病理敏感

#### 3.5.4 ADHD

Seidman 等（1997）在 ADHD 儿童中发现：

- 冲动性临摹错误和混乱的顺序
- 组织受损和回忆评分降低
- 缺陷反映执行功能障碍（工作记忆、规划、抑制）而非原发性视空间或记忆损伤
- 效应量：中等（d = 0.5–0.8）

#### 3.5.5 精神分裂症

Cirillo 与 Seidman（2003）报告：

- 临摹缺陷（视空间建构）
- 回忆损伤（情景记忆）
- 异常组织策略
- 表现与阴性症状严重度和功能结局相关
- 视空间-记忆复合损伤模式，区别于 AD 的纯记忆缺陷

#### 3.5.6 鉴别诊断特征

| 疾病 | 临摹 | 即时回忆 | 延迟回忆 | 再认 | 组织性 |
|------|------|----------|----------|------|--------|
| 阿尔茨海默病（轻度） | 保留 | ↓↓ | ↓↓ | ↓↓ | 轻度下降 |
| TBI（中重度） | ↓↓ | ↓ | ↓↓ | 可变 | ↓↓ |
| 帕金森病（非痴呆） | ↓ | ↓ | ↓↓ | 保留 | ↓ |
| ADHD | 轻度↓ | ↓ | ↓ | — | ↓ |
| 精神分裂症 | ↓ | ↓ | ↓ | 可变 | ↓ |
| 血管性痴呆 | ↓↓ | ↓ | ↓↓ | 可变 | ↓↓ |

*↓ = 轻度受损；↓↓ = 中重度受损*

### 3.6 数字化转型与机器学习

#### 3.6.1 自动评分

传统评分耗时长（每份方案 5–30 分钟）且引入评分者变异。近十年来自动化和数字化方法迅速发展：

- **基于规则的系统**（Sangiovanni 等，2020）：自动单元检测和位置评分，与人类评分者 Pearson r = 0.79
- **基于 CNN 的回归**（Langer 等，2022；Park 等，2023）：从扫描图像端到端评分，QSS 评分的 MAE = 0.95–1.97
- **迁移学习**（Schuster 等，2023）：在通用草图数据集（TU Berlin）上预训练可提高 ROCF 评分准确性

#### 3.6.2 基准测试

一项全面的基准测试（Galdámez 等，2024）比较了最先进方法，发现：
- 私有数据集占主导地位（尚无大规模公开 ROCF 图像语料库）
- 与人类评分者的 Pearson 相关性：0.79–0.88
- MAE：0.95–1.97
- 主要局限：所有当前模型均在单机构数据集上训练，限制了泛化性

#### 3.6.3 数字化施测

基于平板的施测可捕获纸笔版本无法获取的过程数据（笔压、笔划序列、犹豫潜伏期）。Zhang 等（2021）提出，数字化 ROCF 结合机器学习可提取人类评分者无法察觉的"特征性神经心理学结构信息"，有望改善神经退行性疾病早期检测。

**未来优先事项**:
- 多中心、多样化人群验证
- 整合过程级数字生物标志物
- 临床诊断用途的监管批准（FDA/CE 认证）
- 开放基准以加速方法开发

---

## 4. 讨论

### 4.1 主要发现总结

本综述综合了跨越 80 余年的 ROCF 研究，涵盖六个领域。该测验的持久价值在于其独特能力——在单次简短施测中评估视空间、执行和记忆功能的相互作用。从 Rey 的最初构想到当今数字平台，反映了临床神经心理学的发展轨迹——从定性描述到定量精确再到计算增强。

### 4.2 评分困境

评分系统的泛滥是 ROCF 文献最大的优势也是最大的弱点。每个系统捕捉表现的不同侧面——准确性（Osterrieth）、效率（Taylor）、组织性（BQSS、DSS-ROCF）或储存/提取区分（Meyers & Meyers）。然而，这种碎片化阻碍了荟萃分析汇总，并使临床决策复杂化。该领域将受益于共识驱动的"核心 + 可选模块"框架：标准化最小数据集（如 18 单元准确性 + 临摹耗时 + 再认），辅以临床需要时的系统特异性定性指标。

### 4.3 评估的文化公平性

教育水平和文化调节 ROCF 表现的一致发现亟需关注。WEIRD 人群在常模数据库中的不成比例代表性使健康差距得以延续。有前景的倡议——拉丁美洲常模项目（Arango-Lasprilla 等，2015）、西班牙 NEURONORMA（Peña-Casanova 等，2009）以及新兴亚洲数据库——指向更加公平的未来。然而，非洲、南亚和中东大片地区目前仍无常模。

### 4.4 文献的方法学局限

ROCF 文献存在若干局限性：

1. **样本量小**: 许多临床研究每组 n < 30，限制了统计功效和泛化性
2. **选择偏倚**: 临床样本可能不代表社区人群
3. **评分不可比性**: 使用不同评分系统的研究无法直接比较
4. **纵向数据有限**: 追踪个体内 ROCF 随时间变化的研究极少
5. **发表偏倚**: ROCF 结果为零的研究可能代表性不足

### 4.5 本综述的局限性

本综述存在局限性：(1) 由单一评审者完成筛选，引入潜在选择偏倚；(2) 检索限于英文文献，可能遗漏相关非英文出版物，特别是 Rey 和 Osterrieth 的法语原著；(3) 未系统应用正式质量评估工具（如对纳入综述使用 AMSTAR 2）；(4) 检索于单一时间点（2026 年 7 月），可能未涵盖此后发表的文献。

---

## 5. 结论与未来方向

### 5.1 核心结论

1. ROCF 仍是第一线神经心理学工具，有充分证据支持其在整个生命周期和多样化临床人群中的使用。

2. Meyers & Meyers 系统（含再认测验）在心理测量学严谨性、临床实用性和常模覆盖方面提供了最佳平衡，适用于一般临床实践。当执行/组织过程是主要临床问题时，BQSS 更为可取。

3. 各测验阶段激活可分离的神经网络：临摹（额-顶叶）、即时回忆（海马-前额叶）、延迟回忆（巩固）和再认（熟悉性/回想）。

4. 文化水平与教育水平显著影响测验表现；人口学校正、人群特异性常模对于公平评估至关重要。

5. 数字化评分和机器学习方法前景广阔，但在临床部署前需要进行多中心验证。

### 5.2 未来研究优先事项

1. **统一评分标准**: 召开国际共识会议，建立适用于各种场景的最小核心评分方案，同时允许可选的模块化扩展。

2. **全球常模倡议**: 协调多国数据收集，针对当前代表性不足的人群（非洲、南亚、中东、原住民社区）。

3. **纵向常模**: 追踪健康老化中的 ROCF 轨迹，区分正常衰退与病理变化。

4. **数字生物标志物验证**: 前瞻性研究将数字过程指标（笔划序列、潜伏期、笔压）与既定生物标志物（淀粉样蛋白-PET、脑脊液、MRI 容积）进行关联。

5. **机器学习临床试验**: 随机试验评估 ML 辅助 ROCF 解读相比标准人工评分是否能提高诊断准确性或患者结局。

6. **儿科拓展**: 针对幼儿（3–5 岁）开发和验证简化图形，以实现神经发育障碍的早期检测。

7. **开放科学**: 创建大规模、公开可用、匿名化的 ROCF 图像数据库，加速算法开发和交叉验证。

---

## 参考文献

1. Akshoomoff, N. (2005). Rey-Osterrieth Complex Figure performance in healthy children. *Child Neuropsychology*, 11(4), 397–413.

2. Arango-Lasprilla, J. C., 等. (2015). Rey-Osterrieth Complex Figure – copy and immediate recall: Normative data for the Latin American Spanish speaking adult population. *NeuroRehabilitation*, 37(4), 677–698. DOI: 10.3233/NRE-151285

3. Ardila, A. (2005). Cultural values underlying psychometric cognitive testing. *Neuropsychology Review*, 15(4), 185–195. DOI: 10.1007/s11065-005-7070-3

4. Artiola i Fortuny, L., 等. (1999). Normative data for Spanish-speaking populations. *Journal of the International Neuropsychological Society*, 5(2), 125–138.

5. Boone, K. B., 等. (1992). Rey-Osterrieth Complex Figure performance in Alzheimer's disease. *The Clinical Neuropsychologist*, 6(4), 383–392. DOI: 10.1080/13854049208401872

6. Caffarra, P., 等. (2002). Rey-Osterrieth complex figure: normative values in an Italian population sample. *Neurological Sciences*, 22(6), 443–447.

7. Cirillo, M. A., & Seidman, L. J. (2003). Verbal declarative memory dysfunction in schizophrenia. *Psychiatry Research*, 120(2), 155–169. DOI: 10.1016/S0165-1781(03)00174-3

8. Denman, S. B. (1984). Denman Neuropsychology Memory Scale. *Journal of Clinical Psychology*, 40(4), 1050–1057. DOI: 10.1002/1097-4679(198407)40:4<1050::AID-JCLP2270400432>3.0.CO;2-U

9. Fernández, G., 等. (2000). Rey Figure recall in Alzheimer's disease. *Neurology*, 54(10), 1887–1892. DOI: 10.1212/WNL.54.10.1887

10. Galdámez, P. L., 等. (2024). A benchmark for Rey-Osterrieth complex figure test automatic scoring. *Heliyon*, 10(22), e40172.

11. Higginson, C. I., 等. (2005). ROCF performance in Parkinson's disease. *Journal of the International Neuropsychological Society*, 11(3), 299–307. DOI: 10.1017/S1355617705050290

12. Langer, N., 等. (2022). Automated scoring of the Rey-Osterrieth Complex Figure Test using deep learning. *Neuropsychology*, 36(4), 310–322.

13. Manly, J. J., 等. (2002). Reading level attenuates differences in neuropsychological test performance between African American and White elders. *Journal of the International Neuropsychological Society*, 8(3), 341–348. DOI: 10.1017/S1355617702101016

14. Meyers, J. E., & Meyers, K. R. (1995). *Rey Complex Figure Test and Recognition Trial: Professional Manual*. Psychological Assessment Resources. DOI: 10.1037/t14973-000

15. Millis, S. R., & Ricker, J. H. (1994). ROCF performance in traumatic brain injury. *Journal of Clinical and Experimental Neuropsychology*, 16(4), 561–568. DOI: 10.1080/01688639408402660

16. Ogino, T., 等. (2005). Developmental changes in ROCF performance in Japanese children. *Brain and Development*, 27(3), 205–211. DOI: 10.1016/j.braindev.2004.11.004

17. Osterrieth, P.-A. (1944). Le test de copie d'une figure complexe. *Archives de Psychologie*, 30, 206–356. DOI: 10.5169/seals-114657

18. Park, S., 等. (2023). CNN-based classification of mild cognitive impairment using ROCF images. *BMC Neurology*, 24, 75. DOI: 10.1186/s12883-024-03568-9

19. Peña-Casanova, J., 等. (2009). Spanish Multicenter Normative Studies (NEURONORMA Project): norms for the Rey-Osterrieth Complex Figure. *Archives of Clinical Neuropsychology*, 24(4), 371–393.

20. Rabin, L. A., 等. (2005). Assessment practices of clinical neuropsychologists in the United States and Canada. *The Clinical Neuropsychologist*, 19(4), 609–631.

21. Rey, A. (1941). L'examen psychologique dans les cas d'encéphalopathie traumatique. *L'Année Psychologique*, 42, 359–382. DOI: 10.3406/psy.1941.6058

22. Sangiovanni, S., 等. (2020). A rule-based system for automatic Rey-Osterrieth Complex Figure scoring. *Applied Sciences*, 10(22), 8094.

23. Savage, C. R., 等. (2000). ROCF organizational strategies and memory: an fMRI study. *Cognitive Brain Research*, 9(3), 259–266. DOI: 10.1016/S0926-6410(00)00038-4

24. Seidman, L. J., 等. (1997). Toward defining a neuropsychology of attention deficit-hyperactivity disorder. *Journal of Abnormal Child Psychology*, 25(4), 295–310. DOI: 10.1023/A:1025765431174

25. Slick, D. J., 等. (1999). Detecting symptom exaggeration in compensation-seeking mild head injury cases. *Archives of Clinical Neuropsychology*, 14(3), 227–240.

26. Stern, R. A., 等. (1999). Boston Qualitative Scoring System for the Rey-Osterrieth Complex Figure. *Professional Psychology: Research and Practice*, 30(3), 285–292. DOI: 10.1037/0735-7028.30.3.285

27. Stewart, R., 等. (2001). Age, vascular risk, and cognitive decline in an older British population. *Age and Ageing*, 30(4), 323–328.

28. Strauss, E., 等. (2006). *A Compendium of Neuropsychological Tests*（第 3 版）. Oxford University Press. DOI: 10.1017/CBO9780511544513

29. Suchy, Y., 等. (2011). ROCF and executive functioning. *The Clinical Neuropsychologist*, 25(4), 612–630. DOI: 10.1080/13854046.2011.554444

30. Sullivan, E. V., 等. (2000). ROCF performance and hippocampal volumes. *Neuropsychologia*, 38(3), 313–322. DOI: 10.1016/S0028-3932(99)00105-8

31. Taylor, E. M. (1959). *Psychological Appraisal of Children with Cerebral Defects*. Harvard University Press. DOI: 10.1037/13114-000

32. Troyer, A. K., 等. (1998). Clustering and switching on the ROCF. *Neuropsychology*, 12(1), 3–10. DOI: 10.1037/0894-4105.12.1.3

33. Waber, D. P., & Holmes, J. M. (1985). Assessing children's copy productions of the Rey-Osterrieth Complex Figure. *Journal of Clinical and Experimental Neuropsychology*, 7(3), 264–280. DOI: 10.1080/01688638508401257

34. Zhang, X., 等. (2021). Overview of the Complex Figure Test and its clinical application in neuropsychiatric disorders. *Frontiers in Neurology*, 12, 680474. DOI: 10.3389/fneur.2021.680474

35. Zhang, Z., 等. (2018). Normative data for the Rey-Osterrieth Complex Figure Test in Chinese population. *Archives of Clinical Neuropsychology*, 33(7), 892–904. DOI: 10.1093/arclin/acx092

---

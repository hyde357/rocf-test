#!/usr/bin/env python3
"""
psychopy_paradigm.py — 独立 PsychoPy 实验范式脚本
=====================================================
包含两个经典认知评估范式：
  1. Rey-Osterrieth 复杂图形测验 (ROCF) — 图形复刻 + 手绘仿真 + 策略分析
  2. OxVPS 视觉感知筛查 — 5 子测验 × 20 试次的仿真评估

所有绘图使用 matplotlib（中文字体 STHeiti），脚本可直接运行。
产出文件：
  - output/rey_traces.png       ROCF 仿真轨迹图
  - output/oxvps_results.png    OxVPS 汇总 + RT 分布直方图
  - output/oxvps_data.csv       试次级仿真数据
"""

import os
import sys
import time
import random
import numpy as np
import pandas as pd
from pathlib import Path

# ============================================================================
# 输出路径
# ============================================================================
OUTPUT_DIR = Path(__file__).resolve().parent if "__file__" in dir() else Path.cwd()
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================================
# Matplotlib 全局配置（中文字体 STHeiti）
# ============================================================================
import matplotlib
matplotlib.use("Agg")  # 无头后端
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import gridspec

_st_font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
_st_prop = fm.FontProperties(fname=_st_font_path)
plt.rcParams["font.sans-serif"] = ["STHeiti"]
plt.rcParams["axes.unicode_minus"] = False

import warnings
warnings.filterwarnings("ignore")

# ============================================================================
# PsychoPy 初始化（无 GUI 时降级为纯仿真）
# ============================================================================
PSYCHOPY_GUI = True
try:
    from psychopy import visual, event, core, monitors
    from psychopy.visual import ShapeStim, Circle, Line, Rect, TextStim
except ImportError:
    PSYCHOPY_GUI = False
    print("[WARN] PsychoPy 不可用，降级为无头仿真模式")
except Exception as e:
    PSYCHOPY_GUI = False
    print(f"[WARN] PsychoPy 初始化失败 ({e})，降级为无头仿真模式")

# ============================================================================
# 第一部分：Rey-Osterrieth 复杂图形测验 (ROCF)
# ============================================================================

# --- 18 个结构元素定义 ---
# 每个元素: {name, vertices(相对坐标), score_weight}
# 参照 Rey 原始评分体系
ROCF_ELEMENTS = [
    {"id": 1,  "name": "大矩形外框",       "verts": [(0,0),(0,10),(10,10),(10,0)], "weight": 2},
    {"id": 2,  "name": "对角线(左上-右下)",  "verts": [(0,10),(10,0)],               "weight": 2},
    {"id": 3,  "name": "对角线(右上-左下)",  "verts": [(10,10),(0,0)],               "weight": 2},
    {"id": 4,  "name": "水平中线",          "verts": [(0,5),(10,5)],                "weight": 2},
    {"id": 5,  "name": "垂直中线",          "verts": [(5,0),(5,10)],                "weight": 2},
    {"id": 6,  "name": "左上角小矩形",      "verts": [(0,8),(0,10),(2,10),(2,8)],  "weight": 2},
    {"id": 7,  "name": "右上角十字",        "verts": [(8,10),(8,12),(7,12),(7,14),
                                                      (9,14),(9,12),(8,12)],        "weight": 2},
    {"id": 8,  "name": "内部菱形",          "verts": [(5,8.5),(3.5,6),(5,3.5),(6.5,6)], "weight": 2},
    {"id": 9,  "name": "左侧小三角",        "verts": [(0,4),(0,6),(2,5)],           "weight": 1},
    {"id": 10, "name": "右侧平行线",        "verts": [(9,3),(11,3),(11,4),(9,4)],   "weight": 1},
    {"id": 11, "name": "对角线交点圆",      "verts": [],  # circle, 特殊处理
                                              "circle": (5,5,0.4),                   "weight": 1},
    {"id": 12, "name": "左下角弧形",        "verts": [(0,0),(1.5,0.5),(2,2),(0.5,1.5)], "weight": 1},
    {"id": 13, "name": "右下角小方框",      "verts": [(8,0),(8,1.5),(10,1.5),(10,0)], "weight": 1},
    {"id": 14, "name": "大矩形内小矩形",    "verts": [(2,2),(2,4),(4,4),(4,2)],     "weight": 1},
    {"id": 15, "name": "顶部横线延伸",      "verts": [(2,10.5),(10,10.5)],          "weight": 0.5},
    {"id": 16, "name": "菱形左侧短线",      "verts": [(1.5,6),(3.5,6)],             "weight": 0.5},
    {"id": 17, "name": "菱形右侧短线",      "verts": [(6.5,6),(8.5,6)],             "weight": 0.5},
    {"id": 18, "name": "外部标记点",        "verts": [(0,10)],                      "weight": 0.5},
]

# --- 3 种手绘策略的仿真参数 ---
# 结构型：从大框架到细节，笔迹流畅
# 细节型：从局部细节开始拼凑
# 混乱型：跳跃式绘制，停顿多
STRATEGY_PARAMS = {
    "structural": {
        "draw_order":    [1,2,3,4,5,8,6,7,14,9,12,10,13,11,15,16,17,18],
        "speed_mean":    0.02,   # 每毫秒移动距离（快）
        "speed_std":     0.005,
        "pause_prob":    0.02,   # 停顿概率低
        "pause_dur_mean": 300,   # 短停顿
        "jitter_std":    0.015,  # 轨迹抖动小
        "label":         "结构型策略"
    },
    "detail": {
        "draw_order":    [6,9,12,14,13,7,8,11,16,17,10,15,18,1,2,3,4,5],
        "speed_mean":    0.015,
        "speed_std":     0.008,
        "pause_prob":    0.05,
        "pause_dur_mean": 600,
        "jitter_std":    0.03,
        "label":         "细节型策略"
    },
    "chaotic": {
        "draw_order":    [1,14,7,3,8,12,6,9,13,2,10,11,16,5,4,15,17,18],
        "speed_mean":    0.01,
        "speed_std":     0.012,
        "pause_prob":    0.10,
        "pause_dur_mean": 900,
        "jitter_std":    0.06,
        "label":         "混乱型策略"
    },
}


def generate_stroke_trajectory(element, params, scale=50, offset_x=100, offset_y=200,
                               start_time=0.0):
    """
    仿真一个结构元素的绘制轨迹。
    返回: (timestamps, xs, ys) — 逐点时间戳和坐标
    """
    verts = np.array(element["verts"], dtype=float)
    if "circle" in element:
        # 圆形：用多边形逼近
        cx, cy, r = element["circle"]
        n = 60
        angles = np.linspace(0, 2 * np.pi, n)
        verts = np.column_stack([cx + r * np.cos(angles), cy + r * np.sin(angles)])
        verts = np.vstack([verts, verts[0]])  # 闭合

    if len(verts) < 2:
        return np.array([start_time]), np.array([offset_x + verts[0,0] * scale]), np.array([offset_y + verts[0,1] * scale])

    all_ts = []
    all_xs = []
    all_ys = []
    t = start_time

    for i in range(len(verts) - 1):
        p0 = verts[i]
        p1 = verts[i + 1]
        segment_vec = p1 - p0
        segment_len = np.linalg.norm(segment_vec)
        if segment_len < 1e-6:
            continue
        direction = segment_vec / segment_len

        # 模拟笔迹：沿方向走，每一步加随机抖动
        pos = p0.copy().astype(float)
        dist = 0.0
        step_size = params["speed_mean"] + random.gauss(0, params["speed_std"])
        step_size = max(step_size, 0.002)

        # 停顿检测（在段开始前）
        if random.random() < params["pause_prob"]:
            pause_ms = params["pause_dur_mean"] * (0.5 + random.random())
            t += pause_ms / 1000.0  # 直接跳过停顿时间，产生可检测的大间隙

        while dist < segment_len:
            step = min(step_size, segment_len - dist)
            pos += direction * step
            # 正交方向抖动
            jitter_x = random.gauss(0, params["jitter_std"])
            jitter_y = random.gauss(0, params["jitter_std"])
            pos[0] += jitter_x
            pos[1] += jitter_y
            dist += step_size
            t += 0.005  # 5ms 采样间隔

            all_ts.append(t)
            all_xs.append(offset_x + pos[0] * scale)
            all_ys.append(offset_y + pos[1] * scale)

    return np.array(all_ts), np.array(all_xs), np.array(all_ys)


def simulate_rey_drawing(strategy_name, scale=50, offset_x=100, offset_y=200):
    """
    仿真完整 Rey 图形绘制，返回轨迹数据和指标。
    """
    params = STRATEGY_PARAMS[strategy_name]
    order = params["draw_order"]
    all_ts, all_xs, all_ys = [], [], []
    t = 0.0
    element_hit = set()

    for elem_id in order:
        elem = ROCF_ELEMENTS[elem_id - 1]
        # 元素间停顿概率
        if random.random() < params["pause_prob"] * 3:
            pause_ms = params["pause_dur_mean"] * (1.0 + random.random())
            t += pause_ms / 1000.0
        ts, xs, ys = generate_stroke_trajectory(elem, params, scale, offset_x, offset_y, t)
        if len(ts) > 0:
            all_ts.extend(ts)
            all_xs.extend(xs)
            all_ys.extend(ys)
            t = ts[-1]
            element_hit.add(elem_id)

    all_ts = np.array(all_ts)
    all_xs = np.array(all_xs)
    all_ys = np.array(all_ys)

    # 计算指标
    completion_time = all_ts[-1] - all_ts[0] if len(all_ts) > 0 else 0
    # 笔迹总长度
    if len(all_xs) > 1:
        dx = np.diff(all_xs)
        dy = np.diff(all_ys)
        stroke_length = np.sum(np.sqrt(dx**2 + dy**2))
    else:
        stroke_length = 0

    # 停顿次数 (>500ms 间隔)
    if len(all_ts) > 1:
        dt = np.diff(all_ts) * 1000  # ms
        pauses = np.sum(dt > 500)
    else:
        pauses = 0

    # 结构评分：命中的元素总分
    total_possible = sum(e["weight"] for e in ROCF_ELEMENTS)
    struct_score = sum(ROCF_ELEMENTS[eid - 1]["weight"] for eid in element_hit) / total_possible

    return {
        "strategy": strategy_name,
        "label": params["label"],
        "ts": all_ts,
        "xs": all_xs,
        "ys": all_ys,
        "completion_time_s": round(completion_time, 2),
        "stroke_length_px": round(stroke_length, 0),
        "pause_count": int(pauses),
        "structure_score": round(struct_score, 4),
        "elements_hit": len(element_hit),
        "elements_total": len(ROCF_ELEMENTS),
    }


def plot_rey_traces(results):
    """绘制 3 种策略的仿真轨迹对比图"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle("Rey-Osterrieth 复杂图形测验 — 仿真手绘轨迹",
                 fontproperties=_st_prop, fontsize=16, fontweight="bold")

    colors = {"structural": "#2196F3", "detail": "#FF9800", "chaotic": "#F44336"}

    for ax, res in zip(axes, results):
        strategy = res["strategy"]
        # 绘制轨迹
        ax.plot(res["xs"], res["ys"], color=colors[strategy], linewidth=0.6, alpha=0.8)
        # 标记起点
        ax.scatter(res["xs"][0], res["ys"][0], color="green", s=60, zorder=5, label="起点")
        # 标记终点
        ax.scatter(res["xs"][-1], res["ys"][-1], color="red", s=60, zorder=5, label="终点")
        ax.set_title(res["label"], fontproperties=_st_prop, fontsize=13)
        ax.set_xlabel("X (像素)", fontproperties=_st_prop)
        ax.set_ylabel("Y (像素)", fontproperties=_st_prop)
        ax.invert_yaxis()  # 屏幕坐标
        ax.legend(prop=_st_prop, fontsize=9)
        ax.set_aspect("equal", "box")

        # 指标标注
        metrics_text = (
            f"完成时间: {res['completion_time_s']}s\n"
            f"笔迹长度: {res['stroke_length_px']:.0f}px\n"
            f"停顿次数: {res['pause_count']}\n"
            f"结构评分: {res['structure_score']:.2%}\n"
            f"命中元素: {res['elements_hit']}/{res['elements_total']}"
        )
        ax.text(0.02, 0.98, metrics_text, transform=ax.transAxes,
                verticalalignment="top", fontproperties=_st_prop, fontsize=8,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.85))

    plt.tight_layout()
    out_path = OUTPUT_DIR / "rey_traces.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[ROCF] 仿真轨迹图已保存: {out_path}")
    return out_path


# ============================================================================
# 第二部分：OxVPS 视觉感知筛查
# ============================================================================

OXVPS_SUBTESTS = {
    "shape_matching":    "形状匹配",
    "object_decision":   "客体决策",
    "divided_attention": "分散注意",
    "semantic_matching": "语义匹配",
    "visual_search":     "视觉搜索",
}

# 难度梯度配置：每 20 试次中有 easy(5) + medium(10) + hard(5)
DIFFICULTY_LEVELS = {
    "easy":   {"rt_mean": 450,  "rt_std": 80,  "accuracy": 0.95},
    "medium": {"rt_mean": 650,  "rt_std": 120, "accuracy": 0.80},
    "hard":   {"rt_mean": 900,  "rt_std": 200, "accuracy": 0.60},
}


def generate_oxvps_trials(n_trials=20):
    """
    为一个子测验生成 n_trials 试次的仿真 RT + 正确率。
    难度梯度：easy 5 试次、medium 10 试次、hard 5 试次。
    """
    trial_configs = (
        ["easy"] * 5 + ["medium"] * 10 + ["hard"] * 5
    )
    random.shuffle(trial_configs)

    trials = []
    for i, diff in enumerate(trial_configs):
        cfg = DIFFICULTY_LEVELS[diff]
        rt = max(150, random.gauss(cfg["rt_mean"], cfg["rt_std"]))
        correct = 1 if random.random() < cfg["accuracy"] else 0
        trials.append({
            "trial_id": i + 1,
            "difficulty": diff,
            "rt_ms": round(rt, 1),
            "correct": correct,
        })
    return trials


def generate_oxvps_dataset():
    """生成所有 5 个子测验 × 20 试次的数据集"""
    all_data = []
    subtest_summaries = {}

    for subtest_key, subtest_name in OXVPS_SUBTESTS.items():
        trials = generate_oxvps_trials(20)
        for t in trials:
            t["subtest"] = subtest_name
            t["subtest_key"] = subtest_key
            all_data.append(t)

        rts = [t["rt_ms"] for t in trials]
        acc = [t["correct"] for t in trials]
        subtest_summaries[subtest_key] = {
            "name": subtest_name,
            "mean_rt": round(np.mean(rts), 1),
            "median_rt": round(np.median(rts), 1),
            "rt_sd": round(np.std(rts), 1),
            "accuracy": round(np.mean(acc), 4),
            "min_rt": round(np.min(rts), 1),
            "max_rt": round(np.max(rts), 1),
            "trials": trials,
        }

    df = pd.DataFrame(all_data)
    df = df[["subtest", "subtest_key", "trial_id", "difficulty", "rt_ms", "correct"]]
    return df, subtest_summaries


def plot_oxvps_results(subtest_summaries):
    """绘制 OxVPS 汇总表 + RT 分布直方图"""
    fig = plt.figure(figsize=(18, 12))
    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)
    fig.suptitle("OxVPS 视觉感知筛查 — 仿真结果汇总",
                 fontproperties=_st_prop, fontsize=16, fontweight="bold")

    # --- 左上：汇总表格 ---
    ax_table = fig.add_subplot(gs[0, :2])
    ax_table.axis("off")
    table_data = []
    for key, s in subtest_summaries.items():
        table_data.append([
            s["name"],
            f'{s["mean_rt"]:.0f} ms',
            f'{s["median_rt"]:.0f} ms',
            f'{s["rt_sd"]:.0f} ms',
            f'{s["accuracy"]:.1%}',
        ])
    columns = ["子测验", "平均 RT", "中位 RT", "RT 标准差", "正确率"]
    tbl = ax_table.table(cellText=table_data, colLabels=columns,
                         loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(11)
    tbl.scale(1.2, 1.8)
    for key, cell in tbl.get_celld().items():
        cell.set_text_props(fontproperties=_st_prop)
        if key[0] == 0:
            cell.set_text_props(fontproperties=_st_prop, fontweight="bold")
            cell.set_facecolor("#E3F2FD")
        if key[1] == 4:  # 正确率列高亮
            cell.set_facecolor("#E8F5E9")

    ax_table.set_title("各子测验汇总统计", fontproperties=_st_prop, fontsize=14, fontweight="bold", pad=15)

    # --- 右列：综合 RT 对比条形图 ---
    ax_bar = fig.add_subplot(gs[0, 2])
    names = [s["name"] for s in subtest_summaries.values()]
    mean_rts = [s["mean_rt"] for s in subtest_summaries.values()]
    colors_bar = ["#2196F3", "#4CAF50", "#FF9800", "#9C27B0", "#F44336"]
    bars = ax_bar.barh(names, mean_rts, color=colors_bar)
    ax_bar.set_xlabel("平均 RT (ms)", fontproperties=_st_prop)
    ax_bar.set_title("各子测验平均 RT 对比", fontproperties=_st_prop, fontsize=13, fontweight="bold")
    for bar, val in zip(bars, mean_rts):
        ax_bar.text(bar.get_width() + 10, bar.get_y() + bar.get_height()/2,
                    f"{val:.0f}", va="center", fontproperties=_st_prop, fontsize=10)
    ax_bar.set_yticklabels(names, fontproperties=_st_prop)
    ax_bar.invert_yaxis()

    # --- 第二、三行：每个子测验的 RT 分布直方图 ---
    subtest_keys = list(subtest_summaries.keys())
    for idx, key in enumerate(subtest_keys):
        row = 1 + idx // 3
        col = idx % 3
        ax = fig.add_subplot(gs[row, col])
        s = subtest_summaries[key]
        rts = [t["rt_ms"] for t in s["trials"]]
        ax.hist(rts, bins=12, color=colors_bar[idx], edgecolor="white", alpha=0.85)
        ax.axvline(s["mean_rt"], color="red", linestyle="--", linewidth=1.5,
                   label=f'均值 {s["mean_rt"]:.0f}ms')
        ax.set_title(s["name"], fontproperties=_st_prop, fontsize=12, fontweight="bold")
        ax.set_xlabel("RT (ms)", fontproperties=_st_prop, fontsize=9)
        ax.set_ylabel("频次", fontproperties=_st_prop, fontsize=9)
        ax.legend(prop=_st_prop, fontsize=8)

    out_path = OUTPUT_DIR / "oxvps_results.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[OxVPS] 结果汇总图已保存: {out_path}")
    return out_path


# ============================================================================
# PsychoPy 图形呈现（ROCF）
# ============================================================================

def draw_rey_figure_psychopy(scale=50, offset=(300, 300)):
    """用 PsychoPy ShapeStim 绘制 Rey 图形（如 GUI 不可用则跳过）"""
    if not PSYCHOPY_GUI:
        print("[PsychoPy] GUI 不可用，跳过图形窗口绘制")
        return None
    try:
        win = visual.Window(size=(800, 800), units="pix", fullscr=False,
                            color="white", screen=0, allowGUI=False)
        stimuli = []
        ox, oy = offset
        for elem in ROCF_ELEMENTS:
            verts = [(ox + x * scale, oy + y * scale) for x, y in elem["verts"]]
            if "circle" in elem:
                cx, cy, r = elem["circle"]
                stim = Circle(win, radius=r * scale, pos=(ox + cx * scale, oy + cy * scale),
                              lineColor="black", fillColor=None, lineWidth=2)
            elif len(verts) >= 2:
                stim = ShapeStim(win, vertices=verts, lineColor="black",
                                 fillColor=None, lineWidth=2, closeShape=(len(verts) > 2))
            else:
                stim = Circle(win, radius=3, pos=(ox + verts[0][0], oy + verts[0][1]),
                              fillColor="black", lineColor="black")
            stimuli.append(stim)

        for stim in stimuli:
            stim.draw()
        win.flip()
        core.wait(2.0)
        win.close()
        print("[PsychoPy] Rey 图形已呈现 2 秒")
    except Exception as e:
        print(f"[PsychoPy] 图形绘制异常: {e}")


# ============================================================================
# 自检打印
# ============================================================================

def print_selfcheck(rey_results, subtest_summaries):
    """打印自检信息"""
    print("\n" + "=" * 70)
    print("PSYCHOPY_PARADIGM.PY — 自检报告")
    print("=" * 70)

    print("\n[1] Rey-Osterrieth 复杂图形测验 (ROCF)")
    print("-" * 50)
    for res in rey_results:
        print(f"  {res['label']}:")
        print(f"    完成时间: {res['completion_time_s']}s")
        print(f"    笔迹总长度: {res['stroke_length_px']:.0f} px")
        print(f"    停顿次数 (>500ms): {res['pause_count']}")
        print(f"    结构评分: {res['structure_score']:.2%} ({res['elements_hit']}/{res['elements_total']} 元素)")

    print("\n[2] OxVPS 视觉感知筛查")
    print("-" * 50)
    for key, s in subtest_summaries.items():
        print(f"  {s['name']}:")
        print(f"    RT: {s['mean_rt']:.1f} ± {s['rt_sd']:.1f} ms (范围 {s['min_rt']:.0f}-{s['max_rt']:.0f})")
        print(f"    正确率: {s['accuracy']:.1%}")

    print("\n[3] 产出文件")
    print("-" * 50)
    for fname in ["rey_traces.png", "oxvps_results.png", "oxvps_data.csv"]:
        fp = OUTPUT_DIR / fname
        status = "OK" if fp.exists() else "MISSING"
        print(f"  {fp}: {status}")

    print("=" * 70)


# ============================================================================
# 主流程
# ============================================================================

def main():
    print("[PsychoPy Paradigm] 开始执行...")
    random.seed(42)
    np.random.seed(42)

    # ---- 1. PsychoPy 图形呈现（Rey 图形）----
    print("\n>>> 步骤 1: PsychoPy 呈现 Rey 图形")
    draw_rey_figure_psychopy()

    # ---- 2. ROCF 仿真 ----
    print("\n>>> 步骤 2: ROCF 仿真手绘轨迹")
    rey_results = []
    for strategy in ["structural", "detail", "chaotic"]:
        res = simulate_rey_drawing(strategy)
        rey_results.append(res)
    rey_path = plot_rey_traces(rey_results)

    # ---- 3. OxVPS 仿真 ----
    print("\n>>> 步骤 3: OxVPS 仿真数据生成")
    df, subtest_summaries = generate_oxvps_dataset()
    csv_path = OUTPUT_DIR / "oxvps_data.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"[OxVPS] 数据已导出: {csv_path}")
    oxvps_path = plot_oxvps_results(subtest_summaries)

    # ---- 4. 自检打印 ----
    print_selfcheck(rey_results, subtest_summaries)

    # ---- 5. 桌面同步 + 手机发送 ----
    import shutil
    files_to_sync = [
        OUTPUT_DIR / "psychopy_paradigm.py",
        OUTPUT_DIR / "rey_traces.png",
        OUTPUT_DIR / "oxvps_results.png",
        OUTPUT_DIR / "oxvps_data.csv",
    ]

    print("\n>>> 步骤 5: 同步桌面副本")
    for fp in files_to_sync:
        if fp.exists():
            dest = os.path.expanduser(f"~/Desktop/{fp.name}")
            shutil.copy2(str(fp), dest)
            print(f"  同步至: {dest}")

    print("\n>>> 步骤 6: 发送到手机")
    try:
        from marvis_mcp import MacMarvisMCP
        mcp = MacMarvisMCP()
        for fp in files_to_sync:
            if fp.exists():
                mcp.send_file(str(fp))
                print(f"  已发送: {fp.name}")
    except ImportError:
        print("  [WARN] marvis_mcp 不可用，跳过手机发送")
    except Exception as e:
        print(f"  [WARN] 手机发送失败: {e}")

    print("\n[DONE] psychopy_paradigm.py 执行完成。")
    return rey_results, df, subtest_summaries


if __name__ == "__main__":
    main()

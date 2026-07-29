"""
Rey-Osterrieth Complex Figure (ROCF) 测验
使用 ShapeStim 逐元素构建 Rey 复杂图形，支持描摹与延时回忆两阶段。
"""

import math
import time
import os

from psychopy import visual, core, event, data, gui
from psychopy.event import Mouse

# ---------- 18 评分单元 (按传统 ROCF 计分体系) ----------
# 坐标系: 以图形中心为原点，单位 height，图形外接约 0.8x0.6
def build_all_elements(win):
    """返回18个元素列表，每个元素是 ShapeStim (可独立控制是否显示)"""
    elements = []
    W, H = 0.40, 0.30  # 半宽半高

    # 1. 左上角十字 (小十字，在矩形左上角外侧)
    cross_h = visual.ShapeStim(win, vertices=[(-W, 0.02), (-W, -0.02)],
                               lineWidth=2, lineColor='black', closeShape=False)
    cross_v = visual.ShapeStim(win, vertices=[(-W-0.02, 0), (-W+0.02, 0)],
                               lineWidth=2, lineColor='black', closeShape=False)
    elements.append(('1. 左上角十字', [cross_h, cross_v]))

    # 2. 大矩形 (外框)
    rect = visual.Rect(win, width=W*2, height=H*2, lineWidth=2, lineColor='black', fillColor=None)
    elements.append(('2. 大矩形', [rect]))

    # 3. 对角线 (左上-右下, 右上-左下)
    diag1 = visual.ShapeStim(win, vertices=[(-W, H), (W, -H)], lineWidth=2, lineColor='black', closeShape=False)
    diag2 = visual.ShapeStim(win, vertices=[(W, H), (-W, -H)], lineWidth=2, lineColor='black', closeShape=False)
    elements.append(('3. 两条对角线', [diag1, diag2]))

    # 4. 水平中线
    h_mid = visual.ShapeStim(win, vertices=[(-W, 0), (W, 0)], lineWidth=2, lineColor='black', closeShape=False)
    elements.append(('4. 水平中线', [h_mid]))

    # 5. 垂直中线 (上半部分，下半部分)
    v_mid_up = visual.ShapeStim(win, vertices=[(0, H), (0, 0)], lineWidth=2, lineColor='black', closeShape=False)
    v_mid_lo = visual.ShapeStim(win, vertices=[(0, 0), (0, -H)], lineWidth=2, lineColor='black', closeShape=False)
    elements.append(('5. 垂直中线', [v_mid_up, v_mid_lo]))

    # 6. 左侧小矩形 (在左上象限内，约0.15x0.1)
    small_rect = visual.Rect(win, width=0.12, height=0.08, pos=(-W+0.08, H-0.06),
                             lineWidth=2, lineColor='black', fillColor=None)
    elements.append(('6. 左侧小矩形', [small_rect]))

    # 7. 上方水平线段 (小矩形上方)
    h_above = visual.ShapeStim(win, vertices=[(-W, H-0.03), (-W+0.16, H-0.03)],
                               lineWidth=2, lineColor='black', closeShape=False)
    elements.append(('7. 上方短水平线', [h_above]))

    # 8. 左上象限4条平行线
    parallels = []
    for i in range(4):
        x = -W + 0.06 + i * 0.03
        pl = visual.ShapeStim(win, vertices=[(x, H*0.5), (x, 0.01)],
                              lineWidth=1.5, lineColor='black', closeShape=False)
        parallels.append(pl)
    elements.append(('8. 左上4条平行线', parallels))

    # 9. 右上方三角形 (在大矩形右上方外侧)
    tri = visual.ShapeStim(win, vertices=[(W, H*0.5), (W+0.08, H), (W+0.08, H*0.3)],
                           lineWidth=2, lineColor='black', fillColor=None, closeShape=True)
    elements.append(('9. 右上方三角形', [tri]))

    # 10. 右上短垂直线 (三角形右边)
    v_short = visual.ShapeStim(win, vertices=[(W+0.08, H*0.55), (W+0.08, H*0.05)],
                               lineWidth=2, lineColor='black', closeShape=False)
    elements.append(('10. 右上短垂直线', [v_short]))

    # 11. 右下角的圆+三个点
    circle = visual.Circle(win, radius=0.04, pos=(W*0.5, -H*0.7),
                           lineWidth=2, lineColor='black', fillColor=None)
    dots = []
    for angle in [0, math.pi*2/3, math.pi*4/3]:
        dx, dy = math.cos(angle)*0.05, math.sin(angle)*0.05
        dot = visual.Circle(win, radius=0.008, pos=(W*0.5+dx, -H*0.7+dy),
                            lineWidth=0.5, fillColor='black')
        dots.append(dot)
    elements.append(('11. 右下圆+三点', [circle] + dots))

    # 12. 右侧5条平行斜线
    slant_parallels = []
    for i in range(5):
        x_base = W*0.6 + i * 0.025
        slant = visual.ShapeStim(win, vertices=[(x_base, -H*0.3), (x_base+0.02, -H*0.8)],
                                 lineWidth=1.5, lineColor='black', closeShape=False)
        slant_parallels.append(slant)
    elements.append(('12. 右侧5条平行斜线', slant_parallels))

    # 13. 右侧大三角形 (矩形右侧内部)
    big_tri = visual.ShapeStim(win, vertices=[(W, -H*0.4), (W*0.55, -H), (W, -H)],
                               lineWidth=2, lineColor='black', fillColor=None, closeShape=True)
    elements.append(('13. 右侧大三角形', [big_tri]))

    # 14. 菱形 (左下象限)
    diamond_w, diamond_h = 0.05, 0.06
    diamond = visual.ShapeStim(win,
        vertices=[(-W*0.5, -H*0.55+diamond_h), (-W*0.5-diamond_w, -H*0.55),
                  (-W*0.5, -H*0.55-diamond_h), (-W*0.5+diamond_w, -H*0.55)],
        lineWidth=2, lineColor='black', fillColor=None, closeShape=True)
    elements.append(('14. 菱形', [diamond]))

    # 15. 右下角垂直线
    v_bottom = visual.ShapeStim(win, vertices=[(W*0.7, -H*0.5), (W*0.7, -H)],
                                lineWidth=2, lineColor='black', closeShape=False)
    elements.append(('15. 右下角垂直线', [v_bottom]))

    # 16. 右下角水平线
    h_bottom = visual.ShapeStim(win, vertices=[(W*0.7, -H*0.7), (W, -H*0.7)],
                                lineWidth=2, lineColor='black', closeShape=False)
    elements.append(('16. 右下角水平线', [h_bottom]))

    # 17. 左下角十字
    cross2_h = visual.ShapeStim(win, vertices=[(-W*0.4, -H*0.82), (-W*0.4, -H*0.92)],
                                lineWidth=2, lineColor='black', closeShape=False)
    cross2_v = visual.ShapeStim(win, vertices=[(-W*0.44, -H*0.87), (-W*0.36, -H*0.87)],
                                lineWidth=2, lineColor='black', closeShape=False)
    elements.append(('17. 左下角十字', [cross2_h, cross2_v]))

    # 18. 左下角正方形
    square = visual.Rect(win, width=0.06, height=0.06, pos=(-W*0.15, -H*0.87),
                         lineWidth=2, lineColor='black', fillColor=None)
    elements.append(('18. 左下角正方形', [square]))

    return elements


def draw_all(elements):
    """绘制所有元素"""
    for _, shapes in elements:
        for s in shapes:
            s.draw()


# ---------- 主实验流程 ----------
def run_experiment(subject_id="", output_dir="output"):
    # 被试信息
    if not subject_id:
        dlg = gui.Dlg(title="被试信息")
        dlg.addField("被试编号:", "")
        dlg.addField("阶段:", choices=["临摹 (Copy)", "延迟回忆 (Recall)"])
        dlg.show()
        if not dlg.OK:
            core.quit()
        subject_id = dlg.data[0]
        phase = dlg.data[1]
    else:
        phase = "临摹 (Copy)"

    # 窗口
    win = visual.Window(size=[1200, 900], fullscr=False, color=[0.88, 0.88, 0.88],
                        units='height', monitor='testMonitor')

    # 构建图形元素
    elements = build_all_elements(win)

    # ---- 阶段: 指导语 ----
    if "临摹" in phase:
        msg = (
            "接下来屏幕上会呈现 Rey-Osterrieth 复杂图形。\n\n"
            "请在白纸上尽可能准确地临摹这个图形。\n"
            "注意图形的整体结构和细节。\n\n"
            "准备好后按空格键开始。"
        )
    else:
        msg = (
            "请在白纸上凭记忆尽可能准确地画出\n"
            "之前看过的 Rey-Osterrieth 复杂图形。\n\n"
            "准备好后按空格键开始。"
        )

    instr = visual.TextStim(win, text=msg, height=0.04, color='black', wrapWidth=1.2)
    instr.draw()
    win.flip()
    event.waitKeys(keyList=['space', 'escape'])
    if 'escape' in event.getKeys():
        win.close(); core.quit()

    # ---- 阶段: 呈现图形 ----
    mouse = Mouse(win=win)
    start_time = core.getTime()
    draw_all(elements)
    win.flip()

    # 等待被试按空格表示完成临摹（或超时）
    while True:
        keys = event.getKeys(keyList=['space', 'escape'], timeStamped=False)
        if 'escape' in keys:
            win.close(); core.quit()
        if 'space' in keys:
            break
        core.wait(0.05)

    elapsed = core.getTime() - start_time

    # ---- 记录数据 ----
    os.makedirs(output_dir, exist_ok=True)
    data_path = os.path.join(output_dir, f"rocf_{subject_id}_{phase.replace(' ','_')}_{time.strftime('%Y%m%d_%H%M%S')}.csv")
    with open(data_path, 'w') as f:
        f.write("subject_id,phase,draw_time_seconds,timestamp\n")
        f.write(f"{subject_id},{phase},{elapsed:.2f},{time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # ---- 结束 ----
    end_msg = f"阶段完成！\n绘制用时: {elapsed:.1f} 秒\n\n数据已保存至: {os.path.basename(data_path)}"
    end_stim = visual.TextStim(win, text=end_msg, height=0.04, color='black', wrapWidth=1.2)
    end_stim.draw()
    win.flip()
    event.waitKeys(keyList=['space', 'escape'])

    win.close()
    print(f"数据已保存: {data_path}")
    return data_path


if __name__ == "__main__":
    run_experiment()

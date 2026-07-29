"""
Rey-Osterrieth Complex Figure (ROCF) 上机电子化版本
三分区界面 + 电子绘图板 + 标准化流程 + 过程记录 + 自动计分
"""

import math
import time
import os
import json
import copy
from collections import defaultdict

from psychopy import visual, core, event, gui, data as psychopy_data
from psychopy.event import Mouse


# ============================================================
# 第 1 部分：Rey 复杂图形元素构建 (18 评分单元)
# ============================================================

def build_rey_elements(win, pos=(0, 0), scale=0.38):
    """
    构建Rey复杂图形18个评分单元。
    pos: 刺激图中心位置
    scale: 缩放因子
    返回元素列表 + 外框半宽半高
    """
    W, H = scale, scale * 0.75  # 半宽半高
    ox, oy = pos
    elements = []

    # 1. 左上角十字
    e1 = [
        visual.ShapeStim(win, vertices=[(ox-W, oy+0.02), (ox-W, oy-0.02)],
                         lineWidth=2, lineColor='black', closeShape=False),
        visual.ShapeStim(win, vertices=[(ox-W-0.02, oy), (ox-W+0.02, oy)],
                         lineWidth=2, lineColor='black', closeShape=False),
    ]
    elements.append(('1. 左上角十字', e1))

    # 2. 大矩形
    rect = visual.Rect(win, width=W*2, height=H*2, pos=(ox, oy),
                       lineWidth=2, lineColor='black', fillColor=None)
    elements.append(('2. 大矩形', [rect]))

    # 3. 对角线
    diag1 = visual.ShapeStim(win, vertices=[(ox-W, oy+H), (ox+W, oy-H)],
                             lineWidth=2, lineColor='black', closeShape=False)
    diag2 = visual.ShapeStim(win, vertices=[(ox+W, oy+H), (ox-W, oy-H)],
                             lineWidth=2, lineColor='black', closeShape=False)
    elements.append(('3. 两条对角线', [diag1, diag2]))

    # 4. 水平中线
    h_mid = visual.ShapeStim(win, vertices=[(ox-W, oy), (ox+W, oy)],
                              lineWidth=2, lineColor='black', closeShape=False)
    elements.append(('4. 水平中线', [h_mid]))

    # 5. 垂直中线
    v_mid_up = visual.ShapeStim(win, vertices=[(ox, oy+H), (ox, oy)],
                                 lineWidth=2, lineColor='black', closeShape=False)
    v_mid_lo = visual.ShapeStim(win, vertices=[(ox, oy), (ox, oy-H)],
                                 lineWidth=2, lineColor='black', closeShape=False)
    elements.append(('5. 垂直中线', [v_mid_up, v_mid_lo]))

    # 6. 左侧小矩形
    sm_rect = visual.Rect(win, width=0.12*scale/0.38, height=0.08*scale/0.38,
                          pos=(ox-W+0.08*scale/0.38, oy+H-0.06*scale/0.38),
                          lineWidth=2, lineColor='black', fillColor=None)
    elements.append(('6. 左侧小矩形', [sm_rect]))

    # 7. 上方短水平线
    h_above = visual.ShapeStim(win, vertices=[(ox-W, oy+H-0.03*scale/0.38),
                                              (ox-W+0.16*scale/0.38, oy+H-0.03*scale/0.38)],
                                lineWidth=2, lineColor='black', closeShape=False)
    elements.append(('7. 上方短水平线', [h_above]))

    # 8. 左上4条平行线
    parallels = []
    for i in range(4):
        x = ox - W + 0.06*scale/0.38 + i * 0.03*scale/0.38
        pl = visual.ShapeStim(win, vertices=[(x, oy+H*0.5), (x, oy+0.01)],
                              lineWidth=1.5, lineColor='black', closeShape=False)
        parallels.append(pl)
    elements.append(('8. 左上4条平行线', parallels))

    # 9. 右上方三角形
    tri = visual.ShapeStim(win,
        vertices=[(ox+W, oy+H*0.5), (ox+W+0.08*scale/0.38, oy+H),
                  (ox+W+0.08*scale/0.38, oy+H*0.3)],
        lineWidth=2, lineColor='black', fillColor=None, closeShape=True)
    elements.append(('9. 右上方三角形', [tri]))

    # 10. 右上短垂直线
    v_short = visual.ShapeStim(win, vertices=[(ox+W+0.08*scale/0.38, oy+H*0.55),
                                              (ox+W+0.08*scale/0.38, oy+H*0.05)],
                                lineWidth=2, lineColor='black', closeShape=False)
    elements.append(('10. 右上短垂直线', [v_short]))

    # 11. 右下圆+三点
    circle = visual.Circle(win, radius=0.04*scale/0.38, pos=(ox+W*0.5, oy-H*0.7),
                           lineWidth=2, lineColor='black', fillColor=None)
    dots = []
    for angle in [0, math.pi*2/3, math.pi*4/3]:
        dx = math.cos(angle)*0.05*scale/0.38
        dy = math.sin(angle)*0.05*scale/0.38
        dot = visual.Circle(win, radius=0.005, pos=(ox+W*0.5+dx, oy-H*0.7+dy),
                            lineWidth=0.5, fillColor='black')
        dots.append(dot)
    elements.append(('11. 右下圆+三点', [circle] + dots))

    # 12. 右侧5条平行斜线
    slant_p = []
    for i in range(5):
        x_base = ox + W*0.6 + i * 0.025*scale/0.38
        slant = visual.ShapeStim(win, vertices=[(x_base, oy-H*0.3),
                                                (x_base+0.02*scale/0.38, oy-H*0.8)],
                                  lineWidth=1.5, lineColor='black', closeShape=False)
        slant_p.append(slant)
    elements.append(('12. 右侧5条平行斜线', slant_p))

    # 13. 右侧大三角形
    big_tri = visual.ShapeStim(win,
        vertices=[(ox+W, oy-H*0.4), (ox+W*0.55, oy-H), (ox+W, oy-H)],
        lineWidth=2, lineColor='black', fillColor=None, closeShape=True)
    elements.append(('13. 右侧大三角形', [big_tri]))

    # 14. 菱形
    dw = 0.05*scale/0.38
    dh = 0.06*scale/0.38
    diamond = visual.ShapeStim(win,
        vertices=[(ox-W*0.5, oy-H*0.55+dh), (ox-W*0.5-dw, oy-H*0.55),
                  (ox-W*0.5, oy-H*0.55-dh), (ox-W*0.5+dw, oy-H*0.55)],
        lineWidth=2, lineColor='black', fillColor=None, closeShape=True)
    elements.append(('14. 菱形', [diamond]))

    # 15. 右下角垂直线
    v_bot = visual.ShapeStim(win, vertices=[(ox+W*0.7, oy-H*0.5), (ox+W*0.7, oy-H)],
                              lineWidth=2, lineColor='black', closeShape=False)
    elements.append(('15. 右下角垂直线', [v_bot]))

    # 16. 右下角水平线
    h_bot = visual.ShapeStim(win, vertices=[(ox+W*0.7, oy-H*0.7), (ox+W, oy-H*0.7)],
                              lineWidth=2, lineColor='black', closeShape=False)
    elements.append(('16. 右下角水平线', [h_bot]))

    # 17. 左下角十字
    cross_h = visual.ShapeStim(win, vertices=[(ox-W*0.4, oy-H*0.82), (ox-W*0.4, oy-H*0.92)],
                                lineWidth=2, lineColor='black', closeShape=False)
    cross_v = visual.ShapeStim(win, vertices=[(ox-W*0.44, oy-H*0.87), (ox-W*0.36, oy-H*0.87)],
                                lineWidth=2, lineColor='black', closeShape=False)
    elements.append(('17. 左下角十字', [cross_h, cross_v]))

    # 18. 左下角正方形
    sq = visual.Rect(win, width=0.06*scale/0.38, height=0.06*scale/0.38,
                     pos=(ox-W*0.15, oy-H*0.87),
                     lineWidth=2, lineColor='black', fillColor=None)
    elements.append(('18. 左下角正方形', [sq]))

    return elements, W, H


def draw_rey_elements(elements):
    """绘制所有Rey图形元素"""
    for _, shapes in elements:
        for s in shapes:
            s.draw()


# ============================================================
# 第 2 部分：电子绘图画布
# ============================================================

class DrawingCanvas:
    """电子绘图板，管理所有手绘线段"""

    def __init__(self, win, bounds, pen_color='black', bg_color='white'):
        """
        bounds: (left, top, right, bottom) 画布边界 (units: height)
        """
        self.win = win
        self.bounds = bounds
        self.pen_color = pen_color
        self.bg_color = bg_color
        self.bg_rect = visual.Rect(win, pos=((bounds[0]+bounds[2])/2, (bounds[1]+bounds[3])/2),
                                    width=bounds[2]-bounds[0], height=bounds[1]-bounds[3],
                                    fillColor=bg_color, lineColor='#cccccc', lineWidth=1)

        # 存储所有线段 [{'points':[(x,y),...], 'thickness':int, 'time':float}, ...]
        self.strokes = []
        self.current_stroke = None
        self.redo_stack = []

        # 工具状态
        self.pen_thickness = 2  # 1=细, 2=粗
        self.eraser_mode = False

        # 渲染缓存
        self.stroke_stims = []

        # 行为记录
        self.stroke_log = []  # 每条线段的详细记录

    @property
    def center(self):
        return ((self.bounds[0]+self.bounds[2])/2, (self.bounds[1]+self.bounds[3])/2)

    def start_stroke(self, pos):
        self.current_stroke = {
            'points': [pos],
            'thickness': self.pen_thickness,
            'time': time.time(),
            'eraser': self.eraser_mode
        }

    def extend_stroke(self, pos):
        if self.current_stroke:
            self.current_stroke['points'].append(pos)

    def finish_stroke(self):
        if self.current_stroke and len(self.current_stroke['points']) >= 2:
            self.strokes.append(self.current_stroke)
            self._render_stroke(self.current_stroke)
            # 记录到日志
            pts = self.current_stroke['points']
            self.stroke_log.append({
                'stroke_index': len(self.strokes) - 1,
                'start_pos': pts[0],
                'end_pos': pts[-1],
                'num_points': len(pts),
                'duration': time.time() - self.current_stroke['time'],
                'thickness': self.current_stroke['thickness'],
                'eraser': self.current_stroke['eraser'],
                'timestamp': time.time()
            })
            self.redo_stack.clear()
        self.current_stroke = None

    def _render_stroke(self, stroke):
        color = self.bg_color if stroke['eraser'] else self.pen_color
        line_w = stroke['thickness'] * 2 if stroke['eraser'] else stroke['thickness']
        stim = visual.ShapeStim(
            self.win,
            vertices=stroke['points'],
            lineWidth=line_w,
            lineColor=color,
            closeShape=False
        )
        self.stroke_stims.append(stim)

    def undo(self):
        if self.strokes:
            removed = self.strokes.pop()
            self.redo_stack.append(removed)
            self.stroke_stims.pop()
            self._rebuild_stims()

    def redo(self):
        if self.redo_stack:
            restored = self.redo_stack.pop()
            self.strokes.append(restored)
            self._render_stroke(restored)

    def clear_all(self):
        self.strokes.clear()
        self.stroke_stims.clear()
        self.redo_stack.clear()

    def _rebuild_stims(self):
        self.stroke_stims.clear()
        for s in self.strokes:
            self._render_stroke(s)

    def draw(self):
        self.bg_rect.draw()
        for stim in self.stroke_stims:
            stim.draw()

    def get_stroke_count(self):
        return len(self.strokes)

    def get_total_points(self):
        return sum(len(s['points']) for s in self.strokes)

    def get_erase_count(self):
        return sum(1 for s in self.stroke_log if s['eraser'])

    def get_canvas_snapshot(self):
        """返回画布数据用于保存"""
        return {
            'strokes': [{'points': s['points'], 'thickness': s['thickness'],
                         'eraser': s['eraser'], 'time': s['time']}
                        for s in self.strokes],
            'stroke_log': self.stroke_log,
            'total_strokes': len(self.strokes),
            'total_points': self.get_total_points(),
            'erase_count': self.get_erase_count()
        }


# ============================================================
# 第 3 部分：工具栏按钮
# ============================================================

class ToolBar:
    """右侧工具栏"""

    def __init__(self, win, x, y_top, y_bottom, scale=1.0):
        self.win = win
        self.x = x
        self.y_top = y_top
        self.y_bottom = y_bottom
        self.buttons = {}
        self._build_buttons(scale)

    def _build_buttons(self, scale):
        btn_w, btn_h = 0.18 * scale, 0.045 * scale
        gap = 0.012 * scale
        y = self.y_top - btn_h/2

        def add_btn(label, key):
            rect = visual.Rect(self.win, width=btn_w, height=btn_h,
                               pos=(self.x, y), fillColor='#e0e0e0',
                               lineColor='#999999', lineWidth=1)
            txt = visual.TextStim(self.win, text=label, pos=(self.x, y),
                                  height=0.022*scale, color='black', bold=False)
            self.buttons[key] = {'rect': rect, 'text': txt, 'label': label,
                                 'top': y+btn_h/2, 'bottom': y-btn_h/2,
                                 'left': self.x-btn_w/2, 'right': self.x+btn_w/2}
            return y - btn_h - gap

        y = add_btn('画笔 (细)', 'pen_thin')
        y = add_btn('画笔 (粗)', 'pen_thick')
        y = add_btn('橡皮擦', 'eraser')
        y = add_btn('撤销', 'undo')
        add_btn('重做', 'redo')
        y = add_btn('清空画布', 'clear')
        y = add_btn('完成绘图', 'done')

    def get_clicked(self, pos):
        mx, my = pos
        for key, btn in self.buttons.items():
            if (btn['left'] <= mx <= btn['right'] and
                    btn['bottom'] <= my <= btn['top']):
                return key
        return None

    def highlight(self, key, active=True):
        if key in self.buttons:
            self.buttons[key]['rect'].fillColor = '#b0d0ff' if active else '#e0e0e0'

    def draw(self):
        # 工具栏背景
        bg = visual.Rect(self.win,
                         width=0.22, height=self.y_top-self.y_bottom+0.06,
                         pos=(self.x, (self.y_top+self.y_bottom)/2),
                         fillColor='#f5f5f5', lineColor='#cccccc', lineWidth=1)
        bg.draw()
        # 工具栏标题
        title = visual.TextStim(self.win, text='工具栏',
                                pos=(self.x, self.y_top+0.03),
                                height=0.025, color='#555555', bold=True)
        title.draw()
        for btn in self.buttons.values():
            btn['rect'].draw()
            btn['text'].draw()


# ============================================================
# 第 4 部分：干扰任务
# ============================================================

class DistractorTask:
    """延迟期间的干扰任务 - 简单数学题"""

    def __init__(self, win, num_questions=5):
        self.win = win
        self.num_questions = num_questions
        self.questions = self._generate_questions()
        self.current_idx = 0
        self.start_time = None
        self.answers = []

    def _generate_questions(self):
        import random
        qs = []
        for _ in range(self.num_questions):
            a, b = random.randint(11, 99), random.randint(11, 99)
            op = random.choice(['+', '-'])
            answer = a + b if op == '+' else a - b
            qs.append({'q': f'{a} {op} {b} = ?', 'answer': answer})
        return qs

    def run(self, duration_seconds=180):
        """
        运行干扰任务持续 duration_seconds 秒。
        返回答题数据。
        """
        self.start_time = time.time()
        clock = core.Clock()
        while clock.getTime() < duration_seconds:
            if self.current_idx >= len(self.questions):
                # 生成新题目
                self.questions = self._generate_questions()
                self.current_idx = 0

            q = self.questions[self.current_idx]

            # 显示题目
            remaining = int(duration_seconds - clock.getTime())
            q_text = visual.TextStim(self.win,
                                     text=f'干扰任务 - 剩余 {remaining} 秒\n\n{q["q"]}\n\n请输入答案后按回车',
                                     height=0.04, color='black', wrapWidth=1.2)
            q_text.draw()

            # 输入框
            input_box = visual.TextStim(self.win,
                                        text=f'输入: {getattr(self, "_buf", "")}',
                                        height=0.035, color='blue', pos=(0, -0.15))
            input_box.draw()
            self.win.flip()

            # 处理输入
            buf = ""
            while True:
                keys = event.getKeys()
                if not keys:
                    core.wait(0.02)
                    continue

                for k in keys:
                    if k == 'escape':
                        self.answers.append({'q': q['q'], 'answer': None, 'correct': False})
                        self.current_idx += 1
                        return self.answers
                    elif k == 'return':
                        try:
                            user_ans = int(buf) if buf else None
                        except ValueError:
                            user_ans = None
                        correct = user_ans == q['answer'] if user_ans is not None else False
                        self.answers.append({'q': q['q'], 'user_answer': user_ans,
                                             'correct_answer': q['answer'], 'correct': correct})
                        self.current_idx += 1
                        break
                    elif k == 'backspace':
                        buf = buf[:-1]
                    elif k in '0123456789-':
                        buf += k

                    # 更新显示
                    q_text.draw()
                    input_box = visual.TextStim(self.win,
                                                text=f'输入: {buf}',
                                                height=0.035, color='blue', pos=(0, -0.15))
                    input_box.draw()
                    self.win.flip()
                else:
                    continue
                break

        return self.answers


# ============================================================
# 第 5 部分：自动计分
# ============================================================

class AutoScorer:
    """
    简化版自动计分模块。
    基于画布数据评估 18 个评分单元。
    生产环境可接入 ML 模型做精细匹配；此处用启发式规则。
    """

    SCORE_UNITS = [
        '1. 左上角十字', '2. 大矩形', '3. 两条对角线', '4. 水平中线',
        '5. 垂直中线', '6. 左侧小矩形', '7. 上方短水平线', '8. 左上4条平行线',
        '9. 右上方三角形', '10. 右上短垂直线', '11. 右下圆+三点', '12. 右侧5条平行斜线',
        '13. 右侧大三角形', '14. 菱形', '15. 右下角垂直线', '16. 右下角水平线',
        '17. 左下角十字', '18. 左下角正方形'
    ]

    def score(self, canvas_snapshot, phase='copy'):
        """
        返回计分结果。
        canvas_snapshot: DrawingCanvas.get_canvas_snapshot() 的输出
        """
        strokes = canvas_snapshot.get('strokes', [])
        total_points = canvas_snapshot.get('total_points', 0)
        total_strokes = canvas_snapshot.get('total_strokes', 0)
        erase_count = canvas_snapshot.get('erase_count', 0)

        # 启发式评分规则
        unit_scores = {}
        for unit in self.SCORE_UNITS:
            # 简化：根据绘图复杂度估算
            # 实际应用中应使用AI模型匹配每个单元
            unit_scores[unit] = {'drawn': False, 'score': 0, 'shape_ok': False}

        # 基于笔画数和复杂度估算
        complexity_factor = min(1.0, total_strokes / 30.0)
        for i, unit in enumerate(self.SCORE_UNITS):
            # 外框和大结构更可能被画出
            if i < 6:
                sc = 2 if complexity_factor > 0.3 else (1 if complexity_factor > 0.1 else 0)
            else:
                sc = 2 if complexity_factor > 0.6 else (1 if complexity_factor > 0.3 else 0)
            unit_scores[unit] = {
                'drawn': sc > 0,
                'score': sc,
                'shape_ok': sc == 2
            }

        total = sum(u['score'] for u in unit_scores.values())
        max_score = 36

        return {
            'total_score': total,
            'max_score': max_score,
            'percentage': round(total / max_score * 100, 1),
            'unit_scores': unit_scores,
            'total_strokes': total_strokes,
            'total_points': total_points,
            'erase_count': erase_count,
            'phase': phase,
            'assessment_note': self._generate_note(phase, total)
        }

    @staticmethod
    def _generate_note(phase, score):
        if phase == 'copy':
            if score >= 30:
                return '视空间建构能力良好，组织规划水平较高'
            elif score >= 20:
                return '视空间建构能力中等，存在一定组织困难'
            else:
                return '视空间建构能力较弱，建议进一步评估'
        else:
            if score >= 24:
                return '视觉记忆保持良好'
            elif score >= 14:
                return '视觉记忆保持中等水平'
            else:
                return '视觉记忆保持较弱'


# ============================================================
# 第 6 部分：主实验流程
# ============================================================

class ROCFExperiment:
    """ROCF 电子化测验主控"""

    def __init__(self, subject_id='', output_dir='output', delay_minutes=3):
        self.subject_id = subject_id
        self.output_dir = output_dir
        self.delay_minutes = delay_minutes
        self.win = None
        self.session_data = {
            'subject_id': subject_id,
            'date': time.strftime('%Y-%m-%d'),
            'time': time.strftime('%H:%M:%S'),
            'phases': {}
        }
        os.makedirs(output_dir, exist_ok=True)

    def _collect_subject_info(self):
        """收集被试信息"""
        dlg = gui.Dlg(title='被试信息登记')
        dlg.addField('被试编号:', self.subject_id or '')
        dlg.addField('年龄:', '')
        dlg.addField('性别:', choices=['男', '女', '其他'])
        dlg.addField('利手:', choices=['右利手', '左利手', '双利手'])
        dlg.addField('延迟时长(分钟):', str(self.delay_minutes))
        dlg.addField('终端类型:', choices=['电脑(鼠标)', '平板(触控)'])
        dlg.show()
        if not dlg.OK:
            # 对话框被取消时使用默认值继续，避免闪退
            self.subject_id = self.subject_id or 'SUBJ001'
            self.session_data['subject_id'] = self.subject_id
            self.session_data['age'] = ''
            self.session_data['gender'] = ''
            self.session_data['handedness'] = ''
            self.session_data['device'] = ''
            print('[ROCF] 被试信息对话框已取消，使用默认被试编号继续')
            return True

        self.subject_id = dlg.data[0]
        self.session_data['subject_id'] = self.subject_id
        self.session_data['age'] = dlg.data[1]
        self.session_data['gender'] = dlg.data[2]
        self.session_data['handedness'] = dlg.data[3]
        self.delay_minutes = int(dlg.data[4])
        self.session_data['device'] = dlg.data[5]
        return True

    def _show_instructions(self, phase, extra_text=''):
        """显示指导语"""
        instructions = {
            'copy': (
                'Rey-Osterrieth 复杂图形测验 - 临摹阶段\n\n'
                '左侧屏幕显示标准图形，请在中间画布区域\n'
                '使用鼠标/触控笔尽可能准确地临摹整个图形。\n\n'
                '注意：\n'
                '- 右侧工具栏可切换画笔粗细、橡皮擦、撤销\n'
                '- 限时 10 分钟，时间到将自动保存\n'
                '- 临摹完成后点击"完成绘图"按钮\n\n'
                '准备好后按空格键开始。'
            ),
            'recall': (
                'Rey-Osterrieth 复杂图形测验 - 记忆回忆阶段\n\n'
                '现在请凭记忆在画布上绘出刚才看到的图形。\n'
                '左侧不再显示参考图，请尽量回忆全部细节。\n\n'
                '准备好后按空格键开始。'
            )
        }

        msg = instructions.get(phase, '') + extra_text
        text_stim = visual.TextStim(self.win, text=msg, height=0.035,
                                     color='black', wrapWidth=1.2, pos=(0, 0.05))
        text_stim.draw()
        self.win.flip()
        keys = event.waitKeys(keyList=['space', 'escape'])
        return 'escape' not in keys

    def _setup_ui(self):
        """设置三分区界面元素"""
        # 刺激图区 (左上)
        self.stimulus_pos = (-0.55, 0.15)
        self.rey_elements, self.rey_W, self.rey_H = build_rey_elements(
            self.win, pos=self.stimulus_pos, scale=0.25
        )

        # 刺激图区标题和边框
        self.stim_border = visual.Rect(self.win,
                                       width=self.rey_W*2+0.06, height=self.rey_H*2+0.06,
                                       pos=self.stimulus_pos,
                                       lineColor='#888888', lineWidth=1, fillColor=None)
        self.stim_title = visual.TextStim(self.win, text='标准刺激图',
                                          pos=(self.stimulus_pos[0], self.stimulus_pos[1]+self.rey_H+0.04),
                                          height=0.022, color='#555555', bold=True)

        # 画布区 (中间)
        canvas_left = -0.25
        canvas_right = 0.45
        canvas_top = 0.42
        canvas_bottom = -0.42
        self.canvas = DrawingCanvas(self.win,
                                    bounds=(canvas_left, canvas_top, canvas_right, canvas_bottom))
        self.canvas_title = visual.TextStim(self.win, text='绘图画布',
                                            pos=((canvas_left+canvas_right)/2, canvas_top+0.04),
                                            height=0.022, color='#555555', bold=True)

        # 工具栏 (右侧)
        toolbar_x = 0.65
        self.toolbar = ToolBar(self.win, x=toolbar_x, y_top=0.42, y_bottom=-0.42, scale=1.0)

        # 计时器显示
        self.timer_text = visual.TextStim(self.win, text='', pos=(-0.55, -0.45),
                                           height=0.025, color='#cc0000', bold=True)

        # 状态栏
        self.status_text = visual.TextStim(self.win, text='', pos=(0, -0.47),
                                            height=0.02, color='#333333')

    def _draw_ui_frame(self, show_stimulus=True, phase_label=''):
        """绘制界面框架"""
        # 刺激图区
        if show_stimulus:
            self.stim_border.draw()
            self.stim_title.draw()
            draw_rey_elements(self.rey_elements)
        else:
            # 黑屏遮挡
            cover = visual.Rect(self.win,
                                width=self.rey_W*2+0.06, height=self.rey_H*2+0.06,
                                pos=self.stimulus_pos,
                                fillColor='#333333', lineColor='#555555')
            cover.draw()
            hidden_text = visual.TextStim(self.win, text='(记忆阶段)',
                                          pos=self.stimulus_pos, height=0.025, color='#888888')
            hidden_text.draw()

        # 画布
        self.canvas_title.draw()
        self.canvas.draw()

        # 工具栏
        self.toolbar.draw()

        # 计时器
        self.timer_text.draw()

        # 状态
        self.status_text.draw()

    def _run_drawing_phase(self, phase, duration_sec=600, show_stimulus=True):
        """
        运行绘图阶段。
        phase: 'copy' 或 'recall'
        duration_sec: 限时秒数 (默认600=10分钟)
        show_stimulus: 是否显示刺激图
        """
        clock = core.Clock()
        mouse = Mouse(win=self.win)
        self.canvas.clear_all()
        drawing = False
        active_tool = 'pen_thin'
        self.toolbar.highlight('pen_thin', True)

        # 隐藏鼠标指针? 不隐藏，保持可见
        mouse.setVisible(True)

        phase_start_time = time.time()
        done = False

        while not done:
            elapsed = clock.getTime()
            remaining = max(0, duration_sec - elapsed)

            # 超时自动保存
            if remaining <= 0:
                done = True
                self.status_text.text = '时间到！自动保存中...'

            # 更新计时器
            mins, secs = divmod(int(remaining), 60)
            self.timer_text.text = f'剩余时间: {mins:02d}:{secs:02d}'

            # 处理鼠标/触控输入
            mx, my = mouse.getPos()
            buttons_pressed = mouse.getPressed()

            # 检查工具栏点击
            if buttons_pressed[0]:
                tool_key = self.toolbar.get_clicked((mx, my))
                if tool_key == 'done':
                    done = True
                    break
                elif tool_key == 'pen_thin':
                    self.canvas.eraser_mode = False
                    self.canvas.pen_thickness = 2
                    active_tool = 'pen_thin'
                    self.toolbar.highlight('pen_thick', False)
                    self.toolbar.highlight('eraser', False)
                    self.toolbar.highlight('pen_thin', True)
                elif tool_key == 'pen_thick':
                    self.canvas.eraser_mode = False
                    self.canvas.pen_thickness = 4
                    active_tool = 'pen_thick'
                    self.toolbar.highlight('pen_thin', False)
                    self.toolbar.highlight('eraser', False)
                    self.toolbar.highlight('pen_thick', True)
                elif tool_key == 'eraser':
                    self.canvas.eraser_mode = True
                    self.canvas.pen_thickness = 5
                    active_tool = 'eraser'
                    self.toolbar.highlight('pen_thin', False)
                    self.toolbar.highlight('pen_thick', False)
                    self.toolbar.highlight('eraser', True)
                elif tool_key == 'undo':
                    self.canvas.undo()
                    self.status_text.text = '已撤销上一笔'
                elif tool_key == 'redo':
                    self.canvas.redo()
                    self.status_text.text = '已重做'
                elif tool_key == 'clear':
                    self.canvas.clear_all()
                    self.status_text.text = '画布已清空'

            # 检查鼠标是否在画布区域内
            in_canvas = (self.canvas.bounds[0] <= mx <= self.canvas.bounds[2] and
                         self.canvas.bounds[3] <= my <= self.canvas.bounds[1])

            # 画线逻辑
            if in_canvas and buttons_pressed[0] and not drawing:
                # 检查不是工具栏按钮区域
                tool_key = self.toolbar.get_clicked((mx, my))
                if not tool_key:
                    self.canvas.start_stroke((mx, my))
                    drawing = True
                    self.status_text.text = f'绘制中... (笔画 #{self.canvas.get_stroke_count()+1})'

            if drawing and buttons_pressed[0]:
                self.canvas.extend_stroke((mx, my))
            elif drawing and not buttons_pressed[0]:
                self.canvas.finish_stroke()
                drawing = False
                self.status_text.text = f'笔画数: {self.canvas.get_stroke_count()}'

            # 键盘快捷键
            keys = event.getKeys()
            if 'escape' in keys:
                done = True
            if 'z' in keys and 'lctrl' in keys:
                self.canvas.undo()
            if 'y' in keys and 'lctrl' in keys:
                self.canvas.redo()

            # 渲染
            self._draw_ui_frame(show_stimulus=show_stimulus,
                                phase_label='临摹阶段' if phase == 'copy' else '回忆阶段')
            self.win.flip()

        # 保存阶段数据
        phase_data = {
            'phase': phase,
            'duration': time.time() - phase_start_time,
            'show_stimulus': show_stimulus,
            'canvas': self.canvas.get_canvas_snapshot()
        }

        # 截图
        self._draw_ui_frame(show_stimulus=show_stimulus,
                            phase_label='临摹' if phase == 'copy' else '回忆')
        self.win.flip()
        self.win.getMovieFrame()
        screenshot_path = os.path.join(
            self.output_dir,
            f'rocf_{self.subject_id}_{phase}_{time.strftime("%Y%m%d_%H%M%S")}.png'
        )
        self.win.saveMovieFrames(screenshot_path)
        phase_data['screenshot'] = screenshot_path

        self.session_data['phases'][phase] = phase_data
        return phase_data

    def _run_distractor_phase(self):
        """运行干扰任务"""
        self.status_text.text = '干扰任务进行中...请完成屏幕上的数学题'

        text = visual.TextStim(self.win,
                               text='临摹阶段结束。\n\n接下来将进行一项简单任务，\n请保持注意力集中。\n\n按空格键开始。',
                               height=0.04, color='black', wrapWidth=1.2)
        text.draw()
        self.win.flip()
        event.waitKeys(keyList=['space'])

        distractor = DistractorTask(self.win, num_questions=10)
        answers = distractor.run(duration_seconds=self.delay_minutes * 60)
        self.session_data['distractor'] = answers

        # 干扰任务完成提示
        done_text = visual.TextStim(self.win,
                                    text='干扰任务结束。\n\n即将进入记忆回忆阶段。\n\n按空格键继续。',
                                    height=0.04, color='black', wrapWidth=1.2)
        done_text.draw()
        self.win.flip()
        event.waitKeys(keyList=['space'])

    def _generate_report(self):
        """生成测评报告"""
        scorer = AutoScorer()

        phases = self.session_data.get('phases', {})
        copy_data = phases.get('copy', {}).get('canvas', {})
        recall_data = phases.get('recall', {}).get('canvas', {})

        copy_score = scorer.score(copy_data, 'copy') if copy_data else None
        recall_score = scorer.score(recall_data, 'recall') if recall_data else None

        report = {
            'subject_id': self.subject_id,
            'date': self.session_data['date'],
            'copy_score': copy_score,
            'recall_score': recall_score,
            'copy_details': {
                'duration': phases.get('copy', {}).get('duration', 0),
                'strokes': copy_data.get('total_strokes', 0) if copy_data else 0,
                'erase_count': copy_data.get('erase_count', 0) if copy_data else 0,
            },
            'recall_details': {
                'duration': phases.get('recall', {}).get('duration', 0),
                'strokes': recall_data.get('total_strokes', 0) if recall_data else 0,
                'erase_count': recall_data.get('erase_count', 0) if recall_data else 0,
            },
            'distractor': {
                'total_questions': len(self.session_data.get('distractor', [])),
                'correct': sum(1 for a in self.session_data.get('distractor', [])
                              if a.get('correct')),
            }
        }

        self.session_data['report'] = report
        return report

    def _save_data(self):
        """保存所有数据"""
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        base = f'rocf_{self.subject_id}_{timestamp}'

        # JSON 完整数据
        json_path = os.path.join(self.output_dir, f'{base}_data.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.session_data, f, ensure_ascii=False, indent=2, default=str)

        # CSV 汇总
        csv_path = os.path.join(self.output_dir, f'{base}_summary.csv')
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write('subject_id,date,phase,duration_seconds,total_strokes,'
                    'total_points,erase_count,screenshot\n')
            for phase_name in ['copy', 'recall']:
                p = self.session_data.get('phases', {}).get(phase_name, {})
                if p:
                    c = p.get('canvas', {})
                    f.write(f'{self.subject_id},{self.session_data["date"]},'
                            f'{phase_name},{p.get("duration",0):.1f},'
                            f'{c.get("total_strokes",0)},{c.get("total_points",0)},'
                            f'{c.get("erase_count",0)},{p.get("screenshot","")}\n')

        # 报告
        report = self.session_data.get('report', {})
        report_path = os.path.join(self.output_dir, f'{base}_report.txt')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('=' * 60 + '\n')
            f.write(f'  Rey-Osterrieth 复杂图形测验 (ROCF) 测评报告\n')
            f.write('=' * 60 + '\n')
            f.write(f'被试编号: {self.subject_id}\n')
            f.write(f'测验日期: {self.session_data["date"]}\n')
            f.write(f'终端类型: {self.session_data.get("device","未知")}\n\n')

            for name, label in [('copy_score', '临摹得分'), ('recall_score', '回忆得分')]:
                sc = report.get(name)
                if sc:
                    f.write(f'--- {label} ---\n')
                    f.write(f'总分: {sc["total_score"]}/{sc["max_score"]}\n')
                    f.write(f'百分比: {sc["percentage"]}%\n')
                    f.write(f'笔画数: {sc["total_strokes"]}\n')
                    f.write(f'擦除次数: {sc["erase_count"]}\n')
                    f.write(f'评估: {sc["assessment_note"]}\n\n')

            f.write('--- 18单元详细计分 ---\n')
            for phase_key, label in [('copy_score', '临摹'), ('recall_score', '回忆')]:
                sc = report.get(phase_key)
                if sc:
                    f.write(f'\n[{label}]\n')
                    for unit, info in sc.get('unit_scores', {}).items():
                        f.write(f'  {unit}: {info["score"]}/2\n')

        return json_path, csv_path, report_path

    def run(self):
        """运行完整实验流程"""
        print('[ROCF] 启动中...请留意弹出的被试信息登记窗口')

        # Step 1: 创建窗口
        self.win = visual.Window(size=[1400, 900], fullscr=False,
                                  color=[0.92, 0.92, 0.92],
                                  units='height', monitor='testMonitor')

        # Step 2: 收集被试信息
        if not self._collect_subject_info():
            self.win.close()
            return

        # Step 3: 初始化UI
        self._setup_ui()

        # Step 4: 指导语 + 临摹阶段
        if not self._show_instructions('copy'):
            self.win.close()
            return

        print(f'[ROCF] 临摹阶段开始 - 被试 {self.subject_id}')
        self._run_drawing_phase('copy', duration_sec=600, show_stimulus=True)
        print(f'[ROCF] 临摹阶段结束')

        # Step 5: 延迟 + 干扰任务
        self._run_distractor_phase()

        # Step 6: 回忆阶段
        if not self._show_instructions('recall'):
            self.win.close()
            return

        print(f'[ROCF] 回忆阶段开始 - 被试 {self.subject_id}')
        self._run_drawing_phase('recall', duration_sec=600, show_stimulus=False)
        print(f'[ROCF] 回忆阶段结束')

        # Step 7: 生成报告并保存
        self._generate_report()
        json_path, csv_path, report_path = self._save_data()

        # Step 8: 结束画面
        self.win.flip()
        end_text = visual.TextStim(self.win,
                                   text='测验完成！\n\n所有数据已自动保存。\n\n感谢您的参与！\n\n按空格键退出。',
                                   height=0.045, color='black', wrapWidth=1.2)
        end_text.draw()
        self.win.flip()
        event.waitKeys(keyList=['space', 'escape'])

        self.win.close()
        print(f'[ROCF] 数据已保存:')
        print(f'  JSON: {json_path}')
        print(f'  CSV:  {csv_path}')
        print(f'  报告: {report_path}')

        return json_path, csv_path, report_path


# ============================================================
# 入口
# ============================================================

if __name__ == '__main__':
    import sys
    import traceback

    try:
        exp = ROCFExperiment(output_dir='output')
        exp.run()
    except SystemExit:
        pass
    except Exception as e:
        print(f'\n[错误] 程序异常退出: {e}', file=sys.stderr)
        traceback.print_exc()
        # 如果窗口还在，保持显示错误信息
        try:
            from psychopy import visual, event
            win = visual.Window(size=[800, 400], fullscr=False,
                                color=[0.95, 0.9, 0.9], units='height')
            msg = visual.TextStim(win,
                text=f'程序出错:\n\n{str(e)[:200]}\n\n请截图发送此信息。\n按任意键退出。',
                height=0.04, color='#cc0000', wrapWidth=1.3)
            msg.draw()
            win.flip()
            event.waitKeys()
            win.close()
        except Exception:
            pass
        input('\n按回车键退出...')

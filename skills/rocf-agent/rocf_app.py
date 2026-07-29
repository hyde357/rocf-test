"""
ROCF 电子版 - 常驻 GUI 主程序
基于 PsychoPy 事件循环，窗口常驻，支持多被试反复测试。
"""

import math, time, os, json, copy
from psychopy import visual, core, event, gui
from psychopy.event import Mouse


# ============================================================
# Rey 图形元素
# ============================================================

def build_rey_elements(win, pos=(0, 0), scale=0.38):
    W, H = scale, scale * 0.75
    ox, oy = pos
    elements = []

    e1 = [
        visual.ShapeStim(win, vertices=[(ox-W, oy+0.02), (ox-W, oy-0.02)], lineWidth=2, lineColor='black', closeShape=False),
        visual.ShapeStim(win, vertices=[(ox-W-0.02, oy), (ox-W+0.02, oy)], lineWidth=2, lineColor='black', closeShape=False),
    ]
    elements.append(e1)

    rect = visual.Rect(win, width=W*2, height=H*2, pos=(ox, oy), lineWidth=2, lineColor='black', fillColor=None)
    elements.append([rect])

    diag1 = visual.ShapeStim(win, vertices=[(ox-W, oy+H), (ox+W, oy-H)], lineWidth=2, lineColor='black', closeShape=False)
    diag2 = visual.ShapeStim(win, vertices=[(ox+W, oy+H), (ox-W, oy-H)], lineWidth=2, lineColor='black', closeShape=False)
    elements.append([diag1, diag2])

    h_mid = visual.ShapeStim(win, vertices=[(ox-W, oy), (ox+W, oy)], lineWidth=2, lineColor='black', closeShape=False)
    elements.append([h_mid])

    v_mid_up = visual.ShapeStim(win, vertices=[(ox, oy+H), (ox, oy)], lineWidth=2, lineColor='black', closeShape=False)
    v_mid_lo = visual.ShapeStim(win, vertices=[(ox, oy), (ox, oy-H)], lineWidth=2, lineColor='black', closeShape=False)
    elements.append([v_mid_up, v_mid_lo])

    sm_rect = visual.Rect(win, width=0.12*scale/0.38, height=0.08*scale/0.38,
                          pos=(ox-W+0.08*scale/0.38, oy+H-0.06*scale/0.38),
                          lineWidth=2, lineColor='black', fillColor=None)
    elements.append([sm_rect])

    h_above = visual.ShapeStim(win, vertices=[(ox-W, oy+H-0.03*scale/0.38), (ox-W+0.16*scale/0.38, oy+H-0.03*scale/0.38)],
                                lineWidth=2, lineColor='black', closeShape=False)
    elements.append([h_above])

    parallels = []
    for i in range(4):
        x = ox - W + 0.06*scale/0.38 + i * 0.03*scale/0.38
        parallels.append(visual.ShapeStim(win, vertices=[(x, oy+H*0.5), (x, oy+0.01)],
                                          lineWidth=1.5, lineColor='black', closeShape=False))
    elements.append(parallels)

    tri = visual.ShapeStim(win, vertices=[(ox+W, oy+H*0.5), (ox+W+0.08*scale/0.38, oy+H),
                                           (ox+W+0.08*scale/0.38, oy+H*0.3)],
                           lineWidth=2, lineColor='black', fillColor=None, closeShape=True)
    elements.append([tri])

    v_short = visual.ShapeStim(win, vertices=[(ox+W+0.08*scale/0.38, oy+H*0.55), (ox+W+0.08*scale/0.38, oy+H*0.05)],
                                lineWidth=2, lineColor='black', closeShape=False)
    elements.append([v_short])

    circle = visual.Circle(win, radius=0.04*scale/0.38, pos=(ox+W*0.5, oy-H*0.7),
                           lineWidth=2, lineColor='black', fillColor=None)
    dots = []
    for angle in [0, math.pi*2/3, math.pi*4/3]:
        dx, dy = math.cos(angle)*0.05*scale/0.38, math.sin(angle)*0.05*scale/0.38
        dots.append(visual.Circle(win, radius=0.005, pos=(ox+W*0.5+dx, oy-H*0.7+dy),
                                  lineWidth=0.5, fillColor='black'))
    elements.append([circle] + dots)

    slant_p = []
    for i in range(5):
        x_base = ox + W*0.6 + i * 0.025*scale/0.38
        slant_p.append(visual.ShapeStim(win, vertices=[(x_base, oy-H*0.3), (x_base+0.02*scale/0.38, oy-H*0.8)],
                                        lineWidth=1.5, lineColor='black', closeShape=False))
    elements.append(slant_p)

    big_tri = visual.ShapeStim(win, vertices=[(ox+W, oy-H*0.4), (ox+W*0.55, oy-H), (ox+W, oy-H)],
                               lineWidth=2, lineColor='black', fillColor=None, closeShape=True)
    elements.append([big_tri])

    dw, dh = 0.05*scale/0.38, 0.06*scale/0.38
    diamond = visual.ShapeStim(win, vertices=[(ox-W*0.5, oy-H*0.55+dh), (ox-W*0.5-dw, oy-H*0.55),
                                               (ox-W*0.5, oy-H*0.55-dh), (ox-W*0.5+dw, oy-H*0.55)],
                               lineWidth=2, lineColor='black', fillColor=None, closeShape=True)
    elements.append([diamond])

    v_bot = visual.ShapeStim(win, vertices=[(ox+W*0.7, oy-H*0.5), (ox+W*0.7, oy-H)],
                              lineWidth=2, lineColor='black', closeShape=False)
    elements.append([v_bot])

    h_bot = visual.ShapeStim(win, vertices=[(ox+W*0.7, oy-H*0.7), (ox+W, oy-H*0.7)],
                              lineWidth=2, lineColor='black', closeShape=False)
    elements.append([h_bot])

    cross_h = visual.ShapeStim(win, vertices=[(ox-W*0.4, oy-H*0.82), (ox-W*0.4, oy-H*0.92)],
                                lineWidth=2, lineColor='black', closeShape=False)
    cross_v = visual.ShapeStim(win, vertices=[(ox-W*0.44, oy-H*0.87), (ox-W*0.36, oy-H*0.87)],
                                lineWidth=2, lineColor='black', closeShape=False)
    elements.append([cross_h, cross_v])

    sq = visual.Rect(win, width=0.06*scale/0.38, height=0.06*scale/0.38,
                     pos=(ox-W*0.15, oy-H*0.87), lineWidth=2, lineColor='black', fillColor=None)
    elements.append([sq])

    return elements, W, H


# ============================================================
# 绘图画布
# ============================================================

class Canvas:
    def __init__(self, win, bounds):
        self.win = win
        self.bounds = bounds  # left, top, right, bottom
        self.bg = visual.Rect(win, pos=((bounds[0]+bounds[2])/2, (bounds[1]+bounds[3])/2),
                              width=bounds[2]-bounds[0], height=bounds[1]-bounds[3],
                              fillColor='white', lineColor='#cccccc', lineWidth=1)
        self.strokes = []
        self.stims = []
        self.current = None
        self.redo = []
        self.thick = 2
        self.eraser = False
        self.log = []

    def begin(self, pos):
        self.current = {'pts': [pos], 'thick': self.thick, 'eraser': self.eraser, 't': time.time()}

    def move(self, pos):
        if self.current:
            self.current['pts'].append(pos)

    def end(self):
        if self.current and len(self.current['pts']) >= 2:
            self.strokes.append(self.current)
            color = 'white' if self.current['eraser'] else 'black'
            lw = self.current['thick'] * 2 if self.current['eraser'] else self.current['thick']
            s = visual.ShapeStim(self.win, vertices=self.current['pts'],
                                 lineWidth=lw, lineColor=color, closeShape=False)
            self.stims.append(s)
            self.log.append({'n': len(self.strokes)-1, 'npts': len(self.current['pts']),
                             'dur': time.time()-self.current['t'], 'eraser': self.current['eraser']})
            self.redo.clear()
        self.current = None

    def undo(self):
        if self.strokes:
            self.redo.append(self.strokes.pop())
            self.stims.pop()

    def redo(self):
        if self.redo:
            r = self.redo.pop()
            self.strokes.append(r)
            color = 'white' if r['eraser'] else 'black'
            lw = r['thick'] * 2 if r['eraser'] else r['thick']
            self.stims.append(visual.ShapeStim(self.win, vertices=r['pts'],
                                                lineWidth=lw, lineColor=color, closeShape=False))

    def clear(self):
        self.strokes.clear(); self.stims.clear(); self.redo.clear()

    def draw(self):
        self.bg.draw()
        for s in self.stims:
            s.draw()

    def snapshot(self):
        return {'strokes': len(self.strokes), 'log': self.log, 'total_pts': sum(s['npts'] for s in self.log)}

    def inside(self, x, y):
        return self.bounds[0] <= x <= self.bounds[2] and self.bounds[3] <= y <= self.bounds[1]


# ============================================================
# 按钮
# ============================================================

class Button:
    def __init__(self, win, x, y, w, h, label, color='#e0e0e0', text_color='black', text_height=0.025):
        self.win = win
        self.x, self.y, self.w, self.h = x, y, w, h
        self.rect = visual.Rect(win, width=w, height=h, pos=(x, y),
                                fillColor=color, lineColor='#999999', lineWidth=1)
        self.text = visual.TextStim(win, text=label, pos=(x, y), height=text_height,
                                      color=text_color, font='PingFang SC')
        self._label = label

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value
        self.text.text = value

    def draw(self):
        self.rect.draw()
        self.text.draw()

    def hit(self, mx, my):
        return (self.x - self.w/2 <= mx <= self.x + self.w/2 and
                self.y - self.h/2 <= my <= self.y + self.h/2)

    def highlight(self, on):
        self.rect.fillColor = '#b0d0ff' if on else '#e0e0e0'


# ============================================================
# 主界面
# ============================================================

class ROCFApp:
    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.win = None
        self.mouse = None
        self.state = 'menu'  # menu | info | copy | recall
        self.subject = {}
        self.timestamp = ''
        self.copy_data = None
        self.recall_data = None

    def _init_menu(self):
        """主菜单界面"""
        self.title = visual.TextStim(self.win, text='Rey-Osterrieth 复杂图形测验 (ROCF)',
                                     pos=(0, 0.35), height=0.05, color='#222222', bold=True,
                                     font='PingFang SC')
        self.subtitle = visual.TextStim(self.win, text='电子化测评系统 v2.0',
                                        pos=(0, 0.28), height=0.024, color='#666666',
                                        font='PingFang SC')
        self.btns_menu = [
            Button(self.win, 0, 0.15, 0.35, 0.06, '开始新测验', '#4a90d9', 'white', 0.022),
            Button(self.win, 0, 0.05, 0.35, 0.06, '历史记录', '#5cb85c', 'white', 0.022),
            Button(self.win, 0, -0.10, 0.35, 0.06, '退出系统', '#d9534f', 'white', 0.022),
        ]
        self.footer = visual.TextStim(self.win, text=f'数据目录: {self.output_dir}',
                                      pos=(0, -0.40), height=0.018, color='#aaaaaa',
                                      font='PingFang SC')

    def _init_experiment_ui(self):
        """实验三分区界面（临摹/回忆共用）"""
        # 刺激图
        self.stim_pos = (-0.55, 0.15)
        self.rey, self.reyW, self.reyH = build_rey_elements(self.win, pos=self.stim_pos, scale=0.25)
        self.stim_border = visual.Rect(self.win, width=self.reyW*2+0.06, height=self.reyH*2+0.06,
                                        pos=self.stim_pos, lineColor='#888888', lineWidth=1, fillColor=None)
        self.stim_title = visual.TextStim(self.win, text='标准刺激图', pos=(self.stim_pos[0], self.stim_pos[1]+self.reyH+0.04),
                                          height=0.020, color='#555555', bold=True,
                                          font='PingFang SC')

        # 画布
        self.canvas = Canvas(self.win, bounds=(-0.25, 0.42, 0.45, -0.42))
        self.canvas_title = visual.TextStim(self.win, text='绘图画布', pos=(0.10, 0.47),
                                             height=0.020, color='#555555', bold=True,
                                             font='PingFang SC')

        # 工具栏按钮
        bx = 0.68
        self.tool_btns = [
            Button(self.win, bx, 0.38, 0.18, 0.04, '细笔', '#e0e0e0', 'black', 0.018),
            Button(self.win, bx, 0.33, 0.18, 0.04, '粗笔', '#e0e0e0', 'black', 0.018),
            Button(self.win, bx, 0.28, 0.18, 0.04, '橡皮', '#e0e0e0', 'black', 0.018),
            Button(self.win, bx, 0.23, 0.18, 0.04, '撤销', '#e0e0e0', 'black', 0.018),
            Button(self.win, bx, 0.18, 0.18, 0.04, '重做', '#e0e0e0', 'black', 0.018),
            Button(self.win, bx, 0.13, 0.18, 0.04, '清空', '#e0e0e0', 'black', 0.018),
            Button(self.win, bx, 0.05, 0.20, 0.05, '完成绘图', '#5cb85c', 'white', 0.018),
            Button(self.win, bx, -0.05, 0.20, 0.04, '返回菜单', '#d9534f', 'white', 0.018),
        ]
        self.tool_title = visual.TextStim(self.win, text='工具栏', pos=(bx, 0.44),
                                           height=0.022, color='#555555', bold=True,
                                           font='PingFang SC')
        self.tool_bg = visual.Rect(self.win, width=0.24, height=0.90, pos=(bx, 0.0),
                                    fillColor='#f5f5f5', lineColor='#cccccc', lineWidth=1)

        # 计时器
        self.timer_txt = visual.TextStim(self.win, text='', pos=(-0.55, -0.45),
                                          height=0.022, color='#cc0000', bold=True,
                                          font='PingFang SC')
        # 状态
        self.status_txt = visual.TextStim(self.win, text='', pos=(0, -0.47),
                                           height=0.018, color='#333333',
                                           font='PingFang SC')

        # 记忆遮罩
        self.cover = visual.Rect(self.win, width=self.reyW*2+0.06, height=self.reyH*2+0.06,
                                  pos=self.stim_pos, fillColor='#333333', lineColor='#555555')
        self.cover_txt = visual.TextStim(self.win, text='(记忆阶段)', pos=self.stim_pos,
                                          height=0.022, color='#888888',
                                          font='PingFang SC')

        self.phase_label = ''

    # ---------- 主事件循环 ----------

    def run(self):
        self.win = visual.Window(size=[1400, 900], fullscr=False, color=[0.92, 0.92, 0.92],
                                  units='height', monitor='testMonitor')
        self.mouse = Mouse(win=self.win)
        self.mouse.setVisible(True)

        self._init_menu()
        self._init_experiment_ui()

        print('[ROCF] 系统启动，窗口已打开。关闭窗口或点击退出按钮结束。')

        clock = core.Clock()
        drawing = False
        last_click_time = 0

        while True:
            mx, my = self.mouse.getPos()
            pressed = self.mouse.getPressed()
            now = time.time()

            # ---- 菜单状态 ----
            if self.state == 'menu':
                self._draw_menu()
                self.win.flip()

                if pressed[0] and now - last_click_time > 0.3:
                    for i, b in enumerate(self.btns_menu):
                        if b.hit(mx, my):
                            last_click_time = now
                            if i == 0:
                                self._start_new_test()
                            elif i == 1:
                                self._init_history()
                                self.state = 'history'
                            elif i == 2:
                                print('[ROCF] 用户退出')
                                self.win.close()
                                return

            # ---- 信息登记 ----
            elif self.state == 'info':
                dlg = gui.Dlg(title='被试信息登记')
                dlg.addField('被试编号:', '')
                dlg.addField('年龄:', '')
                dlg.addField('性别:', choices=['男', '女', '其他'])
                dlg.addField('利手:', choices=['右利手', '左利手', '双利手'])
                dlg.show()
                if dlg.OK:
                    self.subject = {
                        'id': dlg.data[0] or 'SUBJ001',
                        'age': dlg.data[1],
                        'gender': dlg.data[2],
                        'hand': dlg.data[3],
                    }
                else:
                    self.subject = {'id': 'SUBJ001', 'age': '', 'gender': '', 'hand': ''}
                self.timestamp = time.strftime('%Y%m%d_%H%M%S')
                self.canvas.clear()
                self.phase_label = '临摹阶段'
                self.state = 'copy'
                self._start_clock = time.time()
                print(f'[ROCF] 临摹开始 - {self.subject["id"]}')

            # ---- 临摹阶段 ----
            elif self.state == 'copy':
                elapsed = time.time() - self._start_clock
                remaining = max(0, 600 - elapsed)
                mins, secs = divmod(int(remaining), 60)
                self.timer_txt.text = f'剩余时间: {mins:02d}:{secs:02d}'
                self.status_txt.text = f'{self.phase_label} | 笔画: {len(self.canvas.strokes)}'

                if self._handle_drawing(mx, my, pressed, now, last_click_time):
                    drawing = True
                    continue

                result = self._check_buttons(mx, my, pressed, now, last_click_time, 'copy')
                if result == 'done' or remaining <= 0:
                    self.copy_data = self.canvas.snapshot()
                    self._save_screenshot('copy')
                    print(f'[ROCF] 临摹结束')
                    self._run_distractor()
                    self.canvas.clear()
                    self.phase_label = '回忆阶段（凭记忆）'
                    self._start_clock = time.time()
                    self.state = 'recall'
                    print(f'[ROCF] 回忆开始 - {self.subject["id"]}')
                elif result == 'menu':
                    self.state = 'menu'
                    continue

                self._draw_experiment(show_stimulus=True)
                self.win.flip()

            # ---- 回忆阶段 ----
            elif self.state == 'recall':
                elapsed = time.time() - self._start_clock
                remaining = max(0, 600 - elapsed)
                mins, secs = divmod(int(remaining), 60)
                self.timer_txt.text = f'剩余时间: {mins:02d}:{secs:02d}'
                self.status_txt.text = f'{self.phase_label} | 笔画: {len(self.canvas.strokes)}'

                self._handle_drawing(mx, my, pressed, now, last_click_time)

                result = self._check_buttons(mx, my, pressed, now, last_click_time, 'recall')
                if result == 'done' or remaining <= 0:
                    self.recall_data = self.canvas.snapshot()
                    self._save_screenshot('recall')
                    self._save_and_report()
                    print(f'[ROCF] 回忆结束，返回菜单')
                    self.state = 'menu'
                elif result == 'menu':
                    self.state = 'menu'
                    continue

                self._draw_experiment(show_stimulus=False)
                self.win.flip()

            # ---- 历史记录浏览 ----
            elif self.state == 'history':
                self._draw_history()
                self.win.flip()

                if pressed[0] and now - last_click_time > 0.3:
                    # 返回菜单
                    if self.hist_btn_back.hit(mx, my):
                        last_click_time = now
                        self.state = 'menu'
                        continue

                    if self.history_records:
                        # 上一页
                        if self.hist_btn_prev.hit(mx, my):
                            last_click_time = now
                            if self.history_page > 0:
                                self.history_page -= 1
                                self._update_history_page()
                            continue

                        # 下一页
                        if self.hist_btn_next.hit(mx, my):
                            last_click_time = now
                            total_pages = (len(self.history_records) + self.history_per_page - 1) // self.history_per_page
                            if self.history_page < total_pages - 1:
                                self.history_page += 1
                                self._update_history_page()
                            continue

                        # 点击某行 → 显示详情
                        start = self.history_page * self.history_per_page
                        page_records = self.history_records[start:start + self.history_per_page]
                        for i, b in enumerate(self.hist_rows_btns):
                            if i < len(page_records) and b.hit(mx, my):
                                last_click_time = now
                                self._show_record_detail(page_records[i])
                                break

            # 退出条件
            if event.getKeys(['escape']):
                # escape 不退出，仅在菜单阶段有效
                if self.state == 'menu':
                    print('[ROCF] 用户按ESC退出')
                    self.win.close()
                    return
                elif self.state in ('copy', 'recall', 'history'):
                    self.state = 'menu'
                    print('[ROCF] 返回菜单')

            core.wait(0.03)

    def _draw_menu(self):
        self.title.draw()
        self.subtitle.draw()
        for b in self.btns_menu:
            b.draw()
        self.footer.draw()

    def _draw_experiment(self, show_stimulus):
        # 工具栏背景
        self.tool_bg.draw()
        self.tool_title.draw()
        for b in self.tool_btns:
            b.draw()

        # 刺激图区
        if show_stimulus:
            self.stim_border.draw()
            self.stim_title.draw()
            for shapes in self.rey:
                for s in shapes:
                    s.draw()
        else:
            self.stim_title.draw()
            self.cover.draw()
            self.cover_txt.draw()

        # 画布
        self.canvas_title.draw()
        self.canvas.draw()

        self.timer_txt.draw()
        self.status_txt.draw()

    def _handle_drawing(self, mx, my, pressed, now, last_click_time):
        """处理画线，返回 True 表示在画线中"""
        if self.canvas.inside(mx, my) and pressed[0]:
            # 检查没点到按钮
            hit_btn = False
            for b in self.tool_btns:
                if b.hit(mx, my):
                    hit_btn = True
                    break
            if not hit_btn:
                if self.canvas.current is None:
                    self.canvas.begin((mx, my))
                else:
                    self.canvas.move((mx, my))
                return True
        if not pressed[0] and self.canvas.current is not None:
            self.canvas.end()
        return False

    def _check_buttons(self, mx, my, pressed, now, last_click, phase):
        """检查工具栏点击，返回 'done' / 'menu' / None"""
        if not pressed[0] or now - last_click < 0.3:
            return None
        for i, b in enumerate(self.tool_btns):
            if b.hit(mx, my):
                if b.label == '细笔':
                    self.canvas.thick = 2; self.canvas.eraser = False
                elif b.label == '粗笔':
                    self.canvas.thick = 4; self.canvas.eraser = False
                elif b.label == '橡皮':
                    self.canvas.eraser = True; self.canvas.thick = 5
                elif b.label == '撤销':
                    self.canvas.undo()
                elif b.label == '重做':
                    self.canvas.redo()
                elif b.label == '清空':
                    self.canvas.clear()
                elif b.label == '完成绘图':
                    return 'done'
                elif b.label == '返回菜单':
                    return 'menu'
                return 'tool'
        return None

    def _start_new_test(self):
        self.copy_data = None
        self.recall_data = None
        self.canvas.clear()
        self.state = 'info'

    # ---------- 历史记录浏览 ----------

    def _init_history(self):
        """初始化历史记录——加载所有 JSON 记录并排序"""
        self.history_records = []
        self.history_page = 0
        self.history_per_page = 6
        if os.path.isdir(self.output_dir):
            for f in os.listdir(self.output_dir):
                if f.startswith('rocf_') and f.endswith('.json'):
                    full = os.path.join(self.output_dir, f)
                    try:
                        with open(full, 'r', encoding='utf-8') as fh:
                            d = json.load(fh)
                        d['_file'] = full
                        self.history_records.append(d)
                    except Exception:
                        continue
            self.history_records.sort(key=lambda d: d.get('timestamp', ''), reverse=True)

        # 标题
        self.hist_title = visual.TextStim(self.win, text='历史测验记录',
                                          pos=(0, 0.42), height=0.040, color='#222222',
                                          bold=True, font='PingFang SC')
        # 表头
        self.hist_header = visual.TextStim(self.win,
            text='被试编号          时间               临摹笔画    回忆笔画',
            pos=(0, 0.30), height=0.018, color='#888888',
            font='PingFang SC', alignHoriz='center')

        # 记录行的文本（动态绘制）
        self.hist_rows_texts = []
        for i in range(self.history_per_page):
            t = visual.TextStim(self.win, text='', pos=(0, 0.20 - i * 0.07),
                                height=0.022, color='#333333',
                                font='PingFang SC', alignHoriz='center')
            self.hist_rows_texts.append(t)

        # 行按钮（用于点击选中）
        self.hist_rows_btns = []
        self.hist_row_bgs = []
        for i in range(self.history_per_page):
            b = Button(self.win, 0, 0.20 - i * 0.07, 0.82, 0.055,
                       '', '#ffffff', '#333333', 0.022)
            self.hist_rows_btns.append(b)
            bg = visual.Rect(self.win, width=0.82, height=0.055, pos=(0, 0.20 - i * 0.07),
                             fillColor='#fafafa', lineColor='#e0e0e0', lineWidth=1)
            self.hist_row_bgs.append(bg)

        # 分页按钮
        self.hist_btn_prev = Button(self.win, -0.20, -0.32, 0.18, 0.05,
                                     '上一页', '#e0e0e0', '#333333', 0.020)
        self.hist_btn_next = Button(self.win, 0.20, -0.32, 0.18, 0.05,
                                     '下一页', '#e0e0e0', '#333333', 0.020)
        self.hist_page_label = visual.TextStim(self.win, text='',
                                               pos=(0, -0.32), height=0.020,
                                               color='#888888', font='PingFang SC')
        self.hist_btn_back = Button(self.win, 0, -0.42, 0.20, 0.05,
                                     '返回菜单', '#d9534f', 'white', 0.020)

        # 空状态
        self.hist_empty = visual.TextStim(self.win,
            text='暂无已保存的测验记录。\n\n请先完成一次测验再查看。',
            pos=(0, 0.05), height=0.028, color='#888888',
            font='PingFang SC', alignHoriz='center')

        self._update_history_page()

    def _update_history_page(self):
        """更新当前页的记录文本"""
        start = self.history_page * self.history_per_page
        page_records = self.history_records[start:start + self.history_per_page]
        total_pages = max(1, (len(self.history_records) + self.history_per_page - 1) // self.history_per_page)
        self.hist_page_label.text = f'第 {self.history_page + 1} / {total_pages} 页'

        for i, t in enumerate(self.hist_rows_texts):
            if i < len(page_records):
                r = page_records[i]
                subj = r.get('subject', {})
                copy_strokes = r.get('copy', {}).get('strokes', 0) if r.get('copy') else '-'
                recall_strokes = r.get('recall', {}).get('strokes', 0) if r.get('recall') else '-'
                ts = r.get('timestamp', '')
                ts_display = f'{ts[:4]}-{ts[4:6]}-{ts[6:8]} {ts[9:11]}:{ts[11:13]}' if len(ts) >= 13 else ts
                t.text = f'{subj.get("id","?"):<12}  {ts_display:<16}  {str(copy_strokes):>6}     {str(recall_strokes):>6}'
                t.color = '#333333'
            else:
                t.text = ''

        for i, b in enumerate(self.hist_rows_btns):
            b.label = page_records[i].get('subject', {}).get('id', '') if i < len(page_records) else ''

    def _draw_history(self):
        self.hist_title.draw()
        self.hist_header.draw()

        if not self.history_records:
            self.hist_empty.draw()
        else:
            for t in self.hist_rows_texts:
                t.draw()
            start = self.history_page * self.history_per_page
            page_records = self.history_records[start:start + self.history_per_page]
            for i in range(min(len(page_records), self.history_per_page)):
                self.hist_row_bgs[i].draw()

            self.hist_btn_prev.draw()
            self.hist_btn_next.draw()
            self.hist_page_label.draw()

        self.hist_btn_back.draw()

    def _show_record_detail(self, record):
        """弹窗展示单条记录详情"""
        subj = record.get('subject', {})
        copy_strokes = record.get('copy', {}).get('strokes', 0) if record.get('copy') else 0
        recall_strokes = record.get('recall', {}).get('strokes', 0) if record.get('recall') else 0
        ts = record.get('timestamp', '')
        if len(ts) >= 13:
            ts_display = f'{ts[:4]}-{ts[4:6]}-{ts[6:8]} {ts[9:11]}:{ts[11:13]}:{ts[13:15]}'
        else:
            ts_display = ts

        msg = (f'被试编号: {subj.get("id","未知")}\n'
               f'年龄: {subj.get("age","-")}  性别: {subj.get("gender","-")}  利手: {subj.get("hand","-")}\n'
               f'测试时间: {ts_display}\n\n'
               f'临摹阶段笔画数: {copy_strokes}\n'
               f'回忆阶段笔画数: {recall_strokes}\n\n'
               f'数据文件: {os.path.basename(record.get("_file",""))}')
        self._popup('记录详情', msg)

    def _run_distractor(self):
        """干扰任务（简化版：倒计时）"""
        dur = 60  # 演示用1分钟，实际应3分钟
        clock = core.Clock()
        while clock.getTime() < dur:
            remaining = int(dur - clock.getTime())
            msg = visual.TextStim(self.win,
                                  text=f'干扰任务\n\n休息 {remaining} 秒...\n\n请稍候，不要回忆图形。',
                                  height=0.04, color='black', wrapWidth=1.2,
                                  font='PingFang SC')
            msg.draw()
            self.win.flip()
            if 'escape' in event.getKeys():
                break
            core.wait(0.1)

    def _save_screenshot(self, phase):
        path = os.path.join(self.output_dir,
                           f'rocf_{self.subject["id"]}_{phase}_{self.timestamp}.png')
        self.win.getMovieFrame()
        self.win.saveMovieFrames(path)
        print(f'  截图: {path}')

    def _save_and_report(self):
        path = os.path.join(self.output_dir,
                           f'rocf_{self.subject["id"]}_{self.timestamp}.json')
        data = {
            'subject': self.subject,
            'timestamp': self.timestamp,
            'copy': self.copy_data,
            'recall': self.recall_data,
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        print(f'  数据: {path}')
        self._popup('测验完成',
                    f'被试: {self.subject["id"]}\n\n'
                    f'临摹笔画: {self.copy_data.get("strokes",0) if self.copy_data else "N/A"}\n'
                    f'回忆笔画: {self.recall_data.get("strokes",0) if self.recall_data else "N/A"}\n\n'
                    f'数据已保存。点击确定返回主菜单。')

    def _popup(self, title, msg):
        """PsychoPy 内简易弹窗"""
        # 画遮罩
        overlay = visual.Rect(self.win, width=2, height=2, pos=(0, 0),
                              fillColor='black', opacity=0.5)
        box = visual.Rect(self.win, width=0.80, height=0.62, pos=(0, 0),
                          fillColor='white', lineColor='#999999', lineWidth=2)
        title_stim = visual.TextStim(self.win, text=title, pos=(0, 0.22),
                                      height=0.035, color='#333333', bold=True,
                                      font='PingFang SC')
        msg_stim = visual.TextStim(self.win, text=msg, pos=(0, 0.02),
                                    height=0.022, color='#555555', wrapWidth=0.72,
                                    font='PingFang SC')
        hint = visual.TextStim(self.win, text='点击"确定"继续', pos=(0, -0.22),
                                height=0.020, color='#999999', font='PingFang SC')
        btn = Button(self.win, 0, -0.18, 0.15, 0.05, '确定', '#4a90d9', 'white', 0.022)

        overlay.draw(); box.draw()
        title_stim.draw(); msg_stim.draw(); hint.draw(); btn.draw()
        self.win.flip()

        # 等待触发点击的鼠标松开，防止弹窗瞬间被关闭
        core.wait(0.3)

        # 等待点击确定或敲回车
        while True:
            if self.mouse.getPressed()[0]:
                mx, my = self.mouse.getPos()
                if btn.hit(mx, my):
                    core.wait(0.15)
                    break
            if 'return' in event.getKeys() or 'space' in event.getKeys():
                core.wait(0.15)
                break
            core.wait(0.02)


# ============================================================
# 入口
# ============================================================

if __name__ == '__main__':
    import sys, traceback
    try:
        app = ROCFApp(output_dir='output')
        app.run()
    except Exception as e:
        print(f'\n[错误] {e}', file=sys.stderr)
        traceback.print_exc()
        input('\n按回车退出...')

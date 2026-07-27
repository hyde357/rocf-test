#!/usr/bin/env python3
"""
ROCF 电子版 - PySide6 GUI 主程序
Rey-Osterrieth Complex Figure Test
跨平台版本 (macOS / Windows / Linux)
"""

import sys, os, json, time, math, platform
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QInputDialog,
    QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QComboBox,
    QSizePolicy, QSplitter, QFrame,
)
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF, Signal, QLineF
from PySide6.QtGui import (
    QPainter, QPen, QBrush, QColor, QPainterPath, QFont,
    QFontMetrics, QPolygonF, QMouseEvent, QPaintEvent,
)

# ============================================================
# 跨平台配置
# ============================================================

# 字体回退链
_SYSTEM = platform.system()
if _SYSTEM == "Darwin":
    FONT_FAMILY = "PingFang SC"
elif _SYSTEM == "Windows":
    FONT_FAMILY = "Microsoft YaHei"
else:
    FONT_FAMILY = "Noto Sans CJK SC"  # Linux

# 数据输出目录
if getattr(sys, "frozen", False):
    OUTPUT_DIR = os.path.join(os.path.expanduser("~/Documents"), "ROCF测验数据")
else:
    OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

WINDOW_W, WINDOW_H = 1400, 900
COPY_TIME = 600       # 10 分钟
RECALL_TIME = 600     # 10 分钟
DISTRACT_TIME = 60    # 干扰任务（秒）

STYLE_SHEET = """
QMainWindow { background: #ebebeb; }
QPushButton {
    border: 1px solid #bbb; border-radius: 4px;
    padding: 8px 16px; font-size: 14px; background: #f5f5f5;
}
QPushButton:hover { background: #e0e0e0; }
QPushButton:pressed { background: #d0d0d0; }
QPushButton#btnStart { background: #4a90d9; color: white; border-color: #3a80c9; font-size: 18px; font-weight: bold; }
QPushButton#btnStart:hover { background: #5aa0e9; }
QPushButton#btnHistory { background: #5cb85c; color: white; border-color: #4ca84c; font-size: 18px; }
QPushButton#btnHistory:hover { background: #6cc86c; }
QPushButton#btnExit { background: #d9534f; color: white; border-color: #c9433f; font-size: 18px; }
QPushButton#btnExit:hover { background: #e9635f; }
QPushButton#btnDone { background: #5cb85c; color: white; font-weight: bold; min-width: 120px; }
QPushButton#btnBack { background: #d9534f; color: white; min-width: 100px; }
QPushButton#btnTool { min-width: 80px; padding: 6px 10px; font-size: 13px; }
QPushButton#btnToolActive { background: #4a90d9; color: white; border-color: #3a80c9; min-width: 80px; }
QPushButton#btnToolDone { background: #5cb85c; color: white; font-weight: bold; min-width: 100px; }
QPushButton#btnToolBack { background: #d9534f; color: white; min-width: 100px; }
QLabel#titleLabel { font-size: 26px; font-weight: bold; color: #222; }
QLabel#subtitleLabel { font-size: 14px; color: #666; }
QLabel#footerLabel { font-size: 12px; color: #aaa; }
QLabel#phaseLabel { font-size: 18px; font-weight: bold; color: #333; }
QLabel#timerLabel { font-size: 20px; font-weight: bold; color: #c00; }
QLabel#statusLabel { font-size: 13px; color: #555; }
QLabel#sectionTitle { font-size: 15px; font-weight: bold; color: #555; }
QTableWidget { font-size: 14px; gridline-color: #ddd; }
QTableWidget::item { padding: 6px; }
QHeaderView::section { font-size: 13px; font-weight: bold; background: #f0f0f0; padding: 6px; }
"""


# ============================================================
# Rey 图形绘制组件
# ============================================================

class ReyFigureWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 250)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(self.rect(), QColor("#f8f8f8"))
        p.setPen(QPen(Qt.black, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        title_font = QFont(FONT_FAMILY, 11, QFont.Bold)
        p.setFont(title_font)
        p.setPen(QColor("#555"))
        p.drawText(self.rect().adjusted(0, 4, 0, 0), Qt.AlignHCenter | Qt.AlignTop, "标准刺激图")

        w = self.width()
        h = self.height() - 20
        margin = 30
        dw = w - margin * 2
        dh = h - margin * 2 - 20
        size = min(dw, dh) * 0.92
        ox = w / 2.0
        oy = margin + 10 + dh / 2.0
        s = size / 2.0

        p.setPen(QPen(Qt.black, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        # Element 1: 十字标记
        cx, cy = ox - s, oy - s * 0.75
        p.drawLine(QPointF(cx - 8, cy), QPointF(cx + 8, cy))
        p.drawLine(QPointF(cx, cy - 8), QPointF(cx, cy + 8))

        # Element 2: 大外框矩形
        p.drawRect(QRectF(ox - s, oy - s * 0.75, s * 2, s * 1.5))

        # Element 3: 对角线
        p.drawLine(QPointF(ox - s, oy + s * 0.75), QPointF(ox + s, oy - s * 0.75))
        p.drawLine(QPointF(ox + s, oy + s * 0.75), QPointF(ox - s, oy - s * 0.75))

        # Element 4: 水平中线
        p.drawLine(QPointF(ox - s, oy), QPointF(ox + s, oy))

        # Element 5: 垂直中线
        p.drawLine(QPointF(ox, oy + s * 0.75), QPointF(ox, oy - s * 0.75))

        # Element 6: 左上小矩形
        sm_w, sm_h = s * 0.24, s * 0.16
        sm_x, sm_y = ox - s + sm_w / 2 + s * 0.02, oy - s * 0.75 + sm_h / 2 + s * 0.04
        p.drawRect(QRectF(sm_x - sm_w / 2, sm_y - sm_h / 2, sm_w, sm_h))

        # Element 7: 上方水平短线
        hx = ox - s + sm_w + s * 0.04
        hy = oy - s * 0.75 + sm_h / 2 + s * 0.04
        p.drawLine(QPointF(hx - sm_w / 2, hy), QPointF(hx + sm_w / 2, hy))

        # Element 8: 内部平行线
        px_start = ox - s + s * 0.12
        px_step = s * 0.07
        for i in range(4):
            px = px_start + i * px_step
            p.drawLine(QPointF(px, oy + s * 0.375), QPointF(px, oy + s * 0.02))

        # Element 9: 右上三角形
        tri_x = ox + s + s * 0.18
        tri = QPolygonF([
            QPointF(ox + s, oy + s * 0.375),
            QPointF(tri_x, oy + s * 0.75),
            QPointF(tri_x, oy + s * 0.225),
        ])
        p.drawPolygon(tri)

        # Element 10: 三角形内竖线
        p.drawLine(QPointF(tri_x, oy + s * 0.4125), QPointF(tri_x, oy + s * 0.04))

        # Element 11: 右下圆+三点
        circle_r = s * 0.09
        circle_x = ox + s * 0.5
        circle_y = oy - s * 0.525
        p.drawEllipse(QPointF(circle_x, circle_y), circle_r, circle_r)
        for angle in [0, math.pi * 2 / 3, math.pi * 4 / 3]:
            dx = math.cos(angle) * circle_r * 1.25
            dy = math.sin(angle) * circle_r * 1.25
            p.setBrush(Qt.black)
            p.drawEllipse(QPointF(circle_x + dx, circle_y + dy), 2.5, 2.5)
            p.setBrush(Qt.NoBrush)

        # Element 12: 右下斜线
        sl_x_base = ox + s * 0.6
        sl_y = oy - s * 0.18
        sl_step = s * 0.06
        sl_len = s * 0.15
        for i in range(5):
            sl_x = sl_x_base + i * sl_step
            p.drawLine(QPointF(sl_x, sl_y), QPointF(sl_x, sl_y + sl_len))

        # Element 13: 左下菱形
        dia_x = ox - s * 0.45
        dia_y = oy - s * 0.22
        dia_r = s * 0.06
        dia = QPolygonF([
            QPointF(dia_x, dia_y - dia_r),
            QPointF(dia_x + dia_r, dia_y),
            QPointF(dia_x, dia_y + dia_r),
            QPointF(dia_x - dia_r, dia_y),
        ])
        p.drawPolygon(dia)

        # Element 14-18: 其余标记
        p.drawLine(QPointF(ox + s, oy - s * 0.45), QPointF(ox + s + s * 0.05, oy - s * 0.45))
        p.drawLine(QPointF(ox + s, oy - s * 0.55), QPointF(ox + s + s * 0.05, oy - s * 0.55))
        p.drawLine(QPointF(ox - s, oy + s * 0.38), QPointF(ox - s - s * 0.05, oy + s * 0.38))
        p.drawLine(QPointF(ox - s, oy + s * 0.50), QPointF(ox - s - s * 0.05, oy + s * 0.50))

        p.end()


# ============================================================
# 绘图画布
# ============================================================

class DrawingCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 400)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMouseTracking(True)
        self.setCursor(Qt.CrossCursor)

        self.strokes = []
        self.current_path = None
        self.current_pen = None
        self.current_eraser = False
        self.undo_stack = []

        self.pen_thick = 4
        self.pen_thin = 2
        self.eraser_width = 20
        self.tool = "pen_thin"
        self.drawing = False

    def set_tool(self, tool):
        self.tool = tool
        if tool == "eraser":
            self.setCursor(Qt.BlankCursor)
        else:
            self.setCursor(Qt.CrossCursor)

    def clear(self):
        self.strokes.clear()
        self.undo_stack.clear()
        self.current_path = None
        self.update()

    def undo(self):
        if self.strokes:
            self.undo_stack.append(self.strokes.pop())
            self.update()

    def redo(self):
        if self.undo_stack:
            self.strokes.append(self.undo_stack.pop())
            self.update()

    def stroke_count(self):
        return len(self.strokes)

    def snapshot(self):
        return {"strokes": len(self.strokes)}

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.current_path = QPainterPath()
            self.current_path.moveTo(event.position())
            self.current_eraser = (self.tool == "eraser")

            if self.tool == "pen_thick":
                w = self.pen_thick
            elif self.tool == "pen_thin":
                w = self.pen_thin
            else:
                w = self.eraser_width
            color = Qt.white if self.current_eraser else Qt.black
            self.current_pen = QPen(color, w, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

    def mouseMoveEvent(self, event):
        if self.drawing and self.current_path:
            self.current_path.lineTo(event.position())
            self.update()
        if self.tool == "eraser" and not self.drawing:
            self.update()

    def mouseReleaseEvent(self, event):
        if self.drawing and self.current_path:
            self.strokes.append({
                "path": self.current_path,
                "pen": QPen(self.current_pen),
                "eraser": self.current_eraser,
            })
            self.undo_stack.clear()
            self.current_path = None
            self.drawing = False
            self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(self.rect(), Qt.white)
        p.setPen(QPen(QColor("#ccc"), 1))
        p.drawRect(self.rect().adjusted(0, 0, -1, -1))

        for s in self.strokes:
            p.setPen(s["pen"])
            p.setBrush(Qt.NoBrush)
            p.drawPath(s["path"])

        if self.current_path and self.current_pen:
            p.setPen(self.current_pen)
            p.setBrush(Qt.NoBrush)
            p.drawPath(self.current_path)

        if self.tool == "eraser" and not self.drawing:
            pos = self.mapFromGlobal(self.cursor().pos())
            r = self.eraser_width / 2
            p.setPen(QPen(QColor("#999"), 1, Qt.DashLine))
            p.setBrush(Qt.NoBrush)
            p.drawEllipse(pos, r, r)

        p.end()


# ============================================================
# 干扰任务
# ============================================================

class DistractorWidget(QWidget):
    finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 28px; color: #333;")
        layout.addWidget(self.label)

        self.remaining = DISTRACT_TIME
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)

    def start_countdown(self):
        self.remaining = DISTRACT_TIME
        self._update_label()
        self.timer.start(1000)

    def _tick(self):
        self.remaining -= 1
        self._update_label()
        if self.remaining <= 0:
            self.timer.stop()
            self.finished.emit()

    def _update_label(self):
        self.label.setText(
            f'<p style="font-size:22px;color:#888;">干扰任务</p>'
            f'<p style="font-size:48px;font-weight:bold;color:#333;">{self.remaining}</p>'
            f'<p style="font-size:16px;color:#999;">秒</p>'
            f'<br><p style="font-size:16px;color:#aaa;">休息一下，不要回忆图形</p>'
        )


# ============================================================
# 工具栏
# ============================================================

class ToolBar(QFrame):
    tool_changed = Signal(str)
    undo_clicked = Signal()
    redo_clicked = Signal()
    clear_clicked = Signal()
    done_clicked = Signal()
    back_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(160)
        self.setStyleSheet("QFrame { background: #f5f5f5; border-left: 1px solid #ccc; }")

        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(10, 20, 10, 20)

        title = QLabel("工具栏")
        title.setObjectName("sectionTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(8)

        self.btn_thin = QPushButton("细笔")
        self.btn_thin.setObjectName("btnToolActive")
        self.btn_thin.clicked.connect(lambda: self._select("pen_thin"))
        layout.addWidget(self.btn_thin)

        self.btn_thick = QPushButton("粗笔")
        self.btn_thick.setObjectName("btnTool")
        self.btn_thick.clicked.connect(lambda: self._select("pen_thick"))
        layout.addWidget(self.btn_thick)

        self.btn_eraser = QPushButton("橡皮")
        self.btn_eraser.setObjectName("btnTool")
        self.btn_eraser.clicked.connect(lambda: self._select("eraser"))
        layout.addWidget(self.btn_eraser)

        layout.addSpacing(12)

        self.btn_undo = QPushButton("撤销")
        self.btn_undo.setObjectName("btnTool")
        self.btn_undo.clicked.connect(self.undo_clicked)
        layout.addWidget(self.btn_undo)

        self.btn_redo = QPushButton("重做")
        self.btn_redo.setObjectName("btnTool")
        self.btn_redo.clicked.connect(self.redo_clicked)
        layout.addWidget(self.btn_redo)

        self.btn_clear = QPushButton("清空")
        self.btn_clear.setObjectName("btnTool")
        self.btn_clear.clicked.connect(self.clear_clicked)
        layout.addWidget(self.btn_clear)

        layout.addStretch()

        self.btn_done = QPushButton("完成绘图")
        self.btn_done.setObjectName("btnToolDone")
        self.btn_done.clicked.connect(self.done_clicked)
        layout.addWidget(self.btn_done)

        self.btn_back = QPushButton("返回菜单")
        self.btn_back.setObjectName("btnToolBack")
        self.btn_back.clicked.connect(self.back_clicked)
        layout.addWidget(self.btn_back)

    def _select(self, tool):
        self.btn_thin.setObjectName("btnTool")
        self.btn_thick.setObjectName("btnTool")
        self.btn_eraser.setObjectName("btnTool")
        if tool == "pen_thin":
            self.btn_thin.setObjectName("btnToolActive")
        elif tool == "pen_thick":
            self.btn_thick.setObjectName("btnToolActive")
        else:
            self.btn_eraser.setObjectName("btnToolActive")

        for btn in [self.btn_thin, self.btn_thick, self.btn_eraser]:
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        self.tool_changed.emit(tool)


# ============================================================
# 实验界面
# ============================================================

class ExperimentWidget(QWidget):
    phase_done = Signal(dict)
    back_menu = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.phase = ""
        self.time_limit = 0
        self.elapsed = 0
        self.subject = {}
        self.timestamp = ""

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 0, 10)

        left_panel = QVBoxLayout()

        top_bar = QHBoxLayout()
        self.phase_label = QLabel()
        self.phase_label.setObjectName("phaseLabel")
        top_bar.addWidget(self.phase_label)
        top_bar.addStretch()
        self.timer_label = QLabel()
        self.timer_label.setObjectName("timerLabel")
        top_bar.addWidget(self.timer_label)
        left_panel.addLayout(top_bar)

        self.rey_widget = ReyFigureWidget()
        left_panel.addWidget(self.rey_widget)

        self.status_label = QLabel()
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)
        left_panel.addWidget(self.status_label)

        left_container = QWidget()
        left_container.setLayout(left_panel)
        layout.addWidget(left_container, stretch=3)

        self.canvas = DrawingCanvas()
        layout.addWidget(self.canvas, stretch=2)

        self.toolbar = ToolBar()
        self.toolbar.tool_changed.connect(self.canvas.set_tool)
        self.toolbar.undo_clicked.connect(self.canvas.undo)
        self.toolbar.redo_clicked.connect(self.canvas.redo)
        self.toolbar.clear_clicked.connect(self.canvas.clear)
        self.toolbar.done_clicked.connect(self._on_done)
        self.toolbar.back_clicked.connect(self.back_menu)
        layout.addWidget(self.toolbar)

        self.clock = QTimer(self)
        self.clock.timeout.connect(self._tick)
        self.clock.setInterval(200)

    def start_phase(self, phase, subject, timestamp):
        self.phase = phase
        self.subject = subject
        self.timestamp = timestamp
        self.time_limit = COPY_TIME if phase == "copy" else RECALL_TIME
        self.elapsed = 0
        self.canvas.clear()

        self.phase_label.setText("临摹阶段" if phase == "copy" else "回忆阶段（凭记忆）")
        self.rey_widget.setVisible(phase == "copy")
        self._update_timer()
        self._update_status()
        self.clock.start()

    def _tick(self):
        self.elapsed += 0.2
        self._update_timer()
        self._update_status()
        if self.elapsed >= self.time_limit:
            self.clock.stop()
            self._on_done()

    def _update_timer(self):
        remaining = max(0, int(self.time_limit - self.elapsed))
        m, s = divmod(remaining, 60)
        self.timer_label.setText(f"剩余时间: {m:02d}:{s:02d}")

    def _update_status(self):
        self.status_label.setText(f"笔画: {self.canvas.stroke_count()}")

    def _on_done(self):
        self.clock.stop()
        self.phase_done.emit(self.canvas.snapshot())


# ============================================================
# 历史记录
# ============================================================

class HistoryWidget(QWidget):
    back_menu = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)

        title = QLabel("历史测验记录")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(10)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["被试编号", "测试时间", "临摹笔画", "回忆笔画"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self._show_detail)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        info_label = QLabel("双击某条记录查看详情")
        info_label.setStyleSheet("color:#999;font-size:12px;")
        btn_layout.addWidget(info_label)
        btn_layout.addStretch()
        btn_back = QPushButton("返回菜单")
        btn_back.setObjectName("btnBack")
        btn_back.clicked.connect(self.back_menu)
        btn_layout.addWidget(btn_back)
        layout.addLayout(btn_layout)

    def load_records(self):
        self.table.setRowCount(0)
        records = []
        if os.path.isdir(OUTPUT_DIR):
            for f in os.listdir(OUTPUT_DIR):
                if f.startswith("rocf_") and f.endswith(".json"):
                    try:
                        with open(os.path.join(OUTPUT_DIR, f), "r", encoding="utf-8") as fh:
                            d = json.load(fh)
                        d["_file"] = f
                        records.append(d)
                    except Exception:
                        continue
        records.sort(key=lambda d: d.get("timestamp", ""), reverse=True)

        self.table.setRowCount(len(records))
        for i, r in enumerate(records):
            subj = r.get("subject", {})
            ts = r.get("timestamp", "")
            if len(ts) >= 13:
                ts_d = f"{ts[:4]}-{ts[4:6]}-{ts[6:8]} {ts[9:11]}:{ts[11:13]}"
            else:
                ts_d = ts
            copy_s = r.get("copy", {}).get("strokes", 0) if r.get("copy") else "-"
            recall_s = r.get("recall", {}).get("strokes", 0) if r.get("recall") else "-"

            self.table.setItem(i, 0, QTableWidgetItem(subj.get("id", "?")))
            self.table.setItem(i, 1, QTableWidgetItem(ts_d))
            self.table.setItem(i, 2, QTableWidgetItem(str(copy_s)))
            self.table.setItem(i, 3, QTableWidgetItem(str(recall_s)))

        self._records = records
        return len(records)

    def _show_detail(self, row, col):
        if row < 0 or row >= len(self._records):
            return
        r = self._records[row]
        subj = r.get("subject", {})
        ts = r.get("timestamp", "")
        if len(ts) >= 13:
            ts_d = f"{ts[:4]}-{ts[4:6]}-{ts[6:8]} {ts[9:11]}:{ts[11:13]}:{ts[13:15]}"
        else:
            ts_d = ts
        copy_s = r.get("copy", {}).get("strokes", 0) if r.get("copy") else 0
        recall_s = r.get("recall", {}).get("strokes", 0) if r.get("recall") else 0

        msg = (
            f"被试编号: {subj.get('id', '未知')}\n"
            f"年龄: {subj.get('age', '-')}  性别: {subj.get('gender', '-')}  利手: {subj.get('hand', '-')}\n"
            f"测试时间: {ts_d}\n\n"
            f"临摹阶段笔画数: {copy_s}\n"
            f"回忆阶段笔画数: {recall_s}\n"
        )
        QMessageBox.information(self, "记录详情", msg)


# ============================================================
# 主菜单
# ============================================================

class MenuWidget(QWidget):
    start_test = Signal()
    show_history = Signal()
    exit_app = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)

        title = QLabel("Rey-Osterrieth Complex Figure Test (ROCF)")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("电子化测评系统 v2.0 (Qt)")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        layout.addSpacing(24)

        btn_start = QPushButton("开始新测验")
        btn_start.setObjectName("btnStart")
        btn_start.setFixedSize(280, 50)
        btn_start.clicked.connect(self.start_test)
        layout.addWidget(btn_start, alignment=Qt.AlignCenter)

        btn_history = QPushButton("历史记录")
        btn_history.setObjectName("btnHistory")
        btn_history.setFixedSize(280, 50)
        btn_history.clicked.connect(self.show_history)
        layout.addWidget(btn_history, alignment=Qt.AlignCenter)

        btn_exit = QPushButton("退出系统")
        btn_exit.setObjectName("btnExit")
        btn_exit.setFixedSize(280, 50)
        btn_exit.clicked.connect(self.exit_app)
        layout.addWidget(btn_exit, alignment=Qt.AlignCenter)

        layout.addSpacing(30)
        footer = QLabel(f"数据目录: {OUTPUT_DIR}")
        footer.setObjectName("footerLabel")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)


# ============================================================
# 主窗口
# ============================================================

class ROCFMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ROCF Electronic Assessment System")
        self.resize(WINDOW_W, WINDOW_H)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.menu = MenuWidget()
        self.menu.start_test.connect(self._start_new_test)
        self.menu.show_history.connect(self._show_history)
        self.menu.exit_app.connect(self.close)
        self.stack.addWidget(self.menu)

        self.experiment = ExperimentWidget()
        self.experiment.phase_done.connect(self._on_phase_done)
        self.experiment.back_menu.connect(self._go_menu)
        self.stack.addWidget(self.experiment)

        self.distractor = DistractorWidget()
        self.distractor.finished.connect(self._on_distractor_done)
        self.stack.addWidget(self.distractor)

        self.history = HistoryWidget()
        self.history.back_menu.connect(self._go_menu)
        self.stack.addWidget(self.history)

        self.stack.setCurrentIndex(0)
        self._subject = {}
        self._timestamp = ""
        self._copy_data = None
        self._recall_data = None

    def _go_menu(self):
        self.stack.setCurrentIndex(0)

    def _start_new_test(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("被试信息登记")
        dlg.setMinimumWidth(300)
        layout = QFormLayout(dlg)

        id_edit = QLineEdit()
        id_edit.setPlaceholderText("默认 SUBJ001")
        age_edit = QLineEdit()
        gender_combo = QComboBox()
        gender_combo.addItems(["男", "女", "其他"])
        hand_combo = QComboBox()
        hand_combo.addItems(["右利手", "左利手", "双利手"])

        layout.addRow("被试编号:", id_edit)
        layout.addRow("年龄:", age_edit)
        layout.addRow("性别:", gender_combo)
        layout.addRow("利手:", hand_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        layout.addRow(buttons)

        if dlg.exec() != QDialog.Accepted:
            return

        self._subject = {
            "id": id_edit.text() or "SUBJ001",
            "age": age_edit.text(),
            "gender": gender_combo.currentText(),
            "hand": hand_combo.currentText(),
        }
        self._timestamp = time.strftime("%Y%m%d_%H%M%S")
        self._copy_data = None
        self._recall_data = None

        self.experiment.start_phase("copy", self._subject, self._timestamp)
        self.stack.setCurrentIndex(1)

    def _on_phase_done(self, data):
        if self.experiment.phase == "copy":
            self._copy_data = data
            self._save_screenshot("copy")
            self.distractor.start_countdown()
            self.stack.setCurrentIndex(2)
        else:
            self._recall_data = data
            self._save_screenshot("recall")
            self._save_and_report()

    def _on_distractor_done(self):
        self.experiment.start_phase("recall", self._subject, self._timestamp)
        self.stack.setCurrentIndex(1)

    def _save_screenshot(self, phase):
        pixmap = self.grab()
        path = os.path.join(
            OUTPUT_DIR, f"rocf_{self._subject['id']}_{phase}_{self._timestamp}.png"
        )
        pixmap.save(path, "PNG")
        print(f"  截图: {path}")

    def _save_and_report(self):
        path = os.path.join(
            OUTPUT_DIR, f"rocf_{self._subject['id']}_{self._timestamp}.json"
        )
        data = {
            "subject": self._subject,
            "timestamp": self._timestamp,
            "copy": self._copy_data,
            "recall": self._recall_data,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        print(f"  数据: {path}")

        QMessageBox.information(
            self,
            "测验完成",
            f"被试: {self._subject['id']}\n\n"
            f"临摹笔画: {self._copy_data.get('strokes', 'N/A') if self._copy_data else 'N/A'}\n"
            f"回忆笔画: {self._recall_data.get('strokes', 'N/A') if self._recall_data else 'N/A'}\n\n"
            f"数据已保存。",
        )
        self._go_menu()

    def _show_history(self):
        self.history.load_records()
        self.stack.setCurrentIndex(3)


# ============================================================
# 入口
# ============================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)
    app.setFont(QFont(FONT_FAMILY, 13))
    window = ROCFMainWindow()
    window.show()
    sys.exit(app.exec())

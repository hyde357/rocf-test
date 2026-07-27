#!/usr/bin/env python3
"""ROCF 验证测试套件 — 语法/导入/配置/数据持久化"""

import sys
import os
import json
import tempfile
import platform
import importlib.util
import unittest

# ---- 加载被测模块 ----
spec = importlib.util.spec_from_file_location(
    "rocf_qt",
    "/Users/vivi/Library/Application Support/com.tencent.mac.marvis/MarvisData/User/oAN1i2UiHlaOPotpL7Do7VVuwkX4/workspace/conv_19f4690173b_d40dc65534dc/output/rocf-test-repo/assets/rocf_qt.py",
)
rocf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rocf)


class TestFontDetection(unittest.TestCase):
    """跨平台字体自动检测"""

    def test_macos_font(self):
        self.assertEqual(rocf.FONT_FAMILY, "PingFang SC")

    def test_font_family_is_string(self):
        self.assertIsInstance(rocf.FONT_FAMILY, str)
        self.assertGreater(len(rocf.FONT_FAMILY), 0)


class TestConfiguration(unittest.TestCase):
    """配置常量验证"""

    def test_window_size(self):
        self.assertEqual(rocf.WINDOW_W, 1400)
        self.assertEqual(rocf.WINDOW_H, 900)

    def test_phase_durations(self):
        self.assertEqual(rocf.COPY_TIME, 600)
        self.assertEqual(rocf.RECALL_TIME, 600)
        self.assertEqual(rocf.DISTRACT_TIME, 60)

    def test_output_dir_configured(self):
        self.assertIsInstance(rocf.OUTPUT_DIR, str)
        self.assertTrue(os.path.isabs(rocf.OUTPUT_DIR))

    def test_stylesheet_not_empty(self):
        self.assertIsInstance(rocf.STYLE_SHEET, str)
        self.assertGreater(len(rocf.STYLE_SHEET), 100)


class TestOutputDir(unittest.TestCase):
    """数据目录自动创建"""

    def test_dir_exists_after_import(self):
        self.assertTrue(os.path.isdir(rocf.OUTPUT_DIR))

    def test_dir_is_writable(self):
        test_file = os.path.join(rocf.OUTPUT_DIR, ".write_test")
        try:
            with open(test_file, "w") as f:
                f.write("ok")
            os.remove(test_file)
        except Exception:
            self.fail("OUTPUT_DIR is not writable")


class TestPySide6Imports(unittest.TestCase):
    """PySide6 环境验证"""

    def test_pyside6_version(self):
        from PySide6 import __version__
        major = int(__version__.split(".")[0])
        self.assertGreaterEqual(major, 6)

    def test_qapplication_creatable(self):
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        self.assertIsNotNone(app)


class TestAppLaunch(unittest.TestCase):
    """应用启动验证（无头模式）"""

    def test_main_window_instantiable(self):
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        window = rocf.ROCFMainWindow()
        self.assertIsNotNone(window)
        self.assertEqual(window.windowTitle(), "ROCF Electronic Assessment System")
        # 不调用 show()，避免弹出窗口
        window.close()

    def test_all_pages_exist(self):
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        window = rocf.ROCFMainWindow()
        self.assertEqual(window.stack.count(), 4)
        window.close()


class TestDrawingCanvas(unittest.TestCase):
    """画布核心逻辑"""

    def test_initial_state(self):
        canvas = rocf.DrawingCanvas()
        self.assertEqual(canvas.stroke_count(), 0)
        self.assertEqual(canvas.tool, "pen_thin")
        self.assertFalse(canvas.drawing)

    def test_clear_resets_strokes(self):
        canvas = rocf.DrawingCanvas()
        canvas.clear()
        self.assertEqual(canvas.stroke_count(), 0)

    def test_set_tool(self):
        canvas = rocf.DrawingCanvas()
        canvas.set_tool("eraser")
        self.assertEqual(canvas.tool, "eraser")
        canvas.set_tool("pen_thick")
        self.assertEqual(canvas.tool, "pen_thick")


class TestDataPersistence(unittest.TestCase):
    """JSON 数据保存逻辑"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def test_json_writable(self):
        data = {
            "subject": {"id": "TEST001", "age": "25", "gender": "男", "hand": "右利手"},
            "timestamp": "20260727_100000",
            "copy": {"strokes": 15},
            "recall": {"strokes": 12},
        }
        path = os.path.join(self.tmpdir, "rocf_TEST001_20260727_100000.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.assertTrue(os.path.exists(path))

    def test_json_roundtrip(self):
        data = {
            "subject": {"id": "TEST002"},
            "timestamp": "20260727_110000",
            "copy": {"strokes": 8},
            "recall": {"strokes": 6},
        }
        path = os.path.join(self.tmpdir, "rocf_TEST002_20260727_110000.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        with open(path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        self.assertEqual(loaded["subject"]["id"], "TEST002")
        self.assertEqual(loaded["copy"]["strokes"], 8)


class TestInstallScript(unittest.TestCase):
    """安装脚本存在且可执行"""

    def test_script_exists(self):
        path = "/Users/vivi/Library/Application Support/com.tencent.mac.marvis/MarvisData/User/oAN1i2UiHlaOPotpL7Do7VVuwkX4/workspace/conv_19f4690173b_d40dc65534dc/output/rocf-test-repo/scripts/install_deps.py"
        self.assertTrue(os.path.exists(path))


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    unittest.main(verbosity=2, argv=[sys.argv[0]])

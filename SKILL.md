---
name: rocf-test
description: >
  Rey-Osterrieth Complex Figure Test (ROCF) electronic assessment system — a cross-platform
  PySide6 desktop application for neuropsychological visual memory evaluation. Features include
  Rey figure stimulus display, interactive drawing canvas, timed copy/recall phases, distractor
  countdown, and JSON-based history records. Use this skill when the user wants to (1) install
  or set up the ROCF test, (2) launch or run the assessment, (3) view test history or data,
  (4) customize test parameters (phase durations, window size), (5) troubleshoot runtime
  issues (missing dependencies, font problems, PySide6 errors), or when keywords like
  "ROCF", "Rey-Osterrieth", "瑞氏复杂图形", "视觉记忆测验", "神经心理测验" appear.
---

# ROCF Electronic Assessment System

You are helping the user install, run, and troubleshoot the ROCF electronic assessment tool.
This is a cross-platform PySide6 desktop application for neuropsychological testing.

## Installation

### Automatic (recommended)

```bash
python scripts/install_deps.py
```

### Manual

```bash
pip install PySide6
```

### Verify

```bash
python -c "from PySide6.QtWidgets import QApplication; print('OK')"
```

## Running the Test

```bash
python assets/rocf_qt.py
```

Before running, copy `assets/rocf_qt.py` to a convenient location (e.g., the user's Desktop or
a project folder). The script auto-detects the platform and selects the appropriate font.

## Test Workflow

1. **Main Menu** — Three options: start new test, view history, exit
2. **Subject Registration** — Dialog prompts for participant ID, age, gender, handedness
3. **Copy Phase** (default 10 min) — Participant copies the Rey figure while stimulus is visible
4. **Distractor Task** — Countdown timer prevents rehearsal (default 60 seconds)
5. **Recall Phase** (default 10 min) — Participant draws from memory without stimulus
6. **Completion Report** — Dialog shows stroke counts; data saved to disk

## Data Output

All results go to `~/Documents/ROCF测验数据/`:

| File | Content |
|------|---------|
| `rocf_{ID}_{ts}.json` | Metadata + stroke counts per phase |
| `rocf_{ID}_copy_{ts}.png` | Screenshot of copy phase |
| `rocf_{ID}_recall_{ts}.png` | Screenshot of recall phase |

## Customizing Parameters

Edit `assets/rocf_qt.py` to change these globals near the top:

| Variable | Default | Meaning |
|----------|---------|---------|
| `COPY_TIME` | 600 | Copy phase duration (seconds) |
| `RECALL_TIME` | 600 | Recall phase duration (seconds) |
| `DISTRACT_TIME` | 60 | Distractor countdown (seconds) |
| `WINDOW_W` | 1400 | Window width (pixels) |
| `WINDOW_H` | 900 | Window height (pixels) |

## Troubleshooting

### ModuleNotFoundError: No module named 'PySide6'

Run `pip install PySide6` or `python scripts/install_deps.py`.

### Chinese characters display as boxes (□□□)

Install CJK fonts for the platform:
- **macOS**: Should work out of the box (PingFang SC)
- **Windows**: Microsoft YaHei should be pre-installed; if missing, install from Settings
- **Linux**: `sudo apt install fonts-noto-cjk` (Debian/Ubuntu) or equivalent

### Window too large for screen

Reduce `WINDOW_W` and `WINDOW_H` in `assets/rocf_qt.py` to match the screen resolution.

### XCB / Wayland errors on Linux

Set environment variable before running:
```bash
export QT_QPA_PLATFORM=xcb
python assets/rocf_qt.py
```
Or try:
```bash
export QT_QPA_PLATFORM=wayland
python assets/rocf_qt.py
```

## Viewing Test History

Launch the application and click "历史记录" on the main menu. The table shows all past
tests sorted by date. Double-click any row to see full details for that participant.

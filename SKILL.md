---
name: rocf-test
description: >
  Rey-Osterrieth Complex Figure Test (ROCF) electronic assessment system built with PySide6/Qt.
  A cross-platform psychological assessment tool featuring Rey figure stimulus display,
  drawing canvas, timer, distractor task, and history records. Use this skill when the user
  wants to (1) install or set up the ROCF test application, (2) run or launch the ROCF
  assessment, (3) troubleshoot ROCF test issues, or any other tasks related to this
  psychological assessment tool.
---

# ROCF Electronic Assessment System

Cross-platform Rey-Osterrieth Complex Figure Test (ROCF) built with PySide6. Supports macOS, Windows, and Linux.

## Quick Start

### First-time setup

Run the installer script to install PySide6:

```bash
cd <skill>/scripts && python install_deps.py
```

Or manually:

```bash
pip install PySide6
```

### Run

```bash
python assets/rocf_qt.py
```

Copy the `assets/rocf_qt.py` file to a convenient location for the user (e.g., Desktop or a project folder) before running.

## Application Workflow

1. **Main Menu** - Start new test, view history, or exit
2. **Subject Registration** - Enter participant ID, age, gender, handedness
3. **Copy Phase** (10 min) - Participant copies the Rey figure with stimulus visible
4. **Distractor Task** (60 sec countdown) - Prevents rehearsal
5. **Recall Phase** (10 min) - Participant draws from memory (no stimulus)
6. **Report** - Stroke counts and data saved to `~/Documents/ROCF测验数据/`

## Data Output

All test data saved to `~/Documents/ROCF测验数据/`:
- `rocf_{SUBJID}_{TIMESTAMP}.json` - Test metadata and stroke counts
- `rocf_{SUBJID}_copy_{TIMESTAMP}.png` - Copy phase screenshot
- `rocf_{SUBJID}_recall_{TIMESTAMP}.png` - Recall phase screenshot

## Cross-Platform Notes

- **macOS**: Uses PingFang SC font
- **Windows**: Uses Microsoft YaHei font (pre-installed on Chinese Windows)
- **Linux**: Uses Noto Sans CJK SC (install with `apt install fonts-noto-cjk` if needed)

If Chinese characters display as boxes, install the appropriate CJK font for the platform.

## Customization

Edit `assets/rocf_qt.py` to adjust:
- `COPY_TIME` / `RECALL_TIME` - Phase durations (default 600 seconds)
- `DISTRACT_TIME` - Distractor countdown (default 60 seconds)
- `WINDOW_W` / `WINDOW_H` - Window dimensions (default 1400x900)

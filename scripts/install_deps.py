#!/usr/bin/env python3
"""
ROCF 测验 - 跨平台依赖安装脚本
自动检测操作系统并安装 PySide6
"""

import sys
import subprocess
import platform


def run(cmd):
    print(f"  $ {cmd}")
    subprocess.check_call(cmd, shell=True)


def main():
    print("=" * 60)
    print("  ROCF 电子化测评系统 - 依赖安装")
    print("=" * 60)
    print(f"  操作系统: {platform.system()} {platform.release()}")
    print(f"  Python:   {sys.version.split()[0]}")
    print()

    # 安装 PySide6
    print("[1/1] 安装 PySide6...")
    run(f"{sys.executable} -m pip install PySide6")

    print()
    print("=" * 60)
    print("  安装完成。运行方式：")
    print(f"    {sys.executable} rocf_qt.py")
    print("=" * 60)


if __name__ == "__main__":
    main()

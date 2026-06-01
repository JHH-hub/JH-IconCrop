# -*- coding: utf-8 -*-
"""
Icon 裁剪工具 - 启动器
双击 exe 后：
  1. 把内嵌的 HTML 释放到系统临时目录
  2. 调用默认浏览器打开
  3. 自身退出（浏览器独立运行）
"""
import os
import sys
import tempfile
import webbrowser
import time


def resource_path(relative_path: str) -> str:
    """
    获取资源文件路径：
      - 开发环境：脚本同目录
      - PyInstaller 打包后：_MEIPASS 临时解压目录
    """
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except AttributeError:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)


def main():
    html_src = resource_path("icon裁剪工具.html")
    if not os.path.isfile(html_src):
        # 兜底：启动失败提示
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(
                0,
                f"找不到内嵌 HTML 文件：\n{html_src}",
                "Icon 裁剪工具 - 启动失败",
                0x10,
            )
        except Exception:
            print(f"[ERROR] HTML not found: {html_src}")
        sys.exit(1)

    # 释放到固定位置，避免每次打开都生成新文件
    target_dir = os.path.join(tempfile.gettempdir(), "IconCropper")
    os.makedirs(target_dir, exist_ok=True)
    target_html = os.path.join(target_dir, "icon裁剪工具.html")

    # 复制（每次覆盖，保证是最新版）
    try:
        with open(html_src, "rb") as fr, open(target_html, "wb") as fw:
            fw.write(fr.read())
    except Exception as e:
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(
                0,
                f"释放 HTML 文件失败：\n{e}",
                "Icon 裁剪工具 - 启动失败",
                0x10,
            )
        except Exception:
            print(f"[ERROR] copy failed: {e}")
        sys.exit(1)

    # 用默认浏览器打开
    url = "file:///" + target_html.replace("\\", "/")
    webbrowser.open(url)

    # 给浏览器一点启动时间再退出（避免某些浏览器没启动完就退）
    time.sleep(0.8)


if __name__ == "__main__":
    main()

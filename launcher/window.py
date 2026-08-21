"""
Window creation and visual setup for the KAIROS launcher.
"""

from __future__ import annotations

import ctypes
import sys
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path

from launcher.utils import LauncherConfig


@dataclass(frozen=True)
class Theme:
    """
    Launcher color system.
    """

    background: str = "#050505"
    surface: str = "#101010"
    red: str = "#D71920"
    red_dark: str = "#7A0C11"
    text: str = "#F4F4F4"
    muted: str = "#8A8A8A"


class WindowFactory:
    """
    Create consistently themed launcher windows.
    """

    def __init__(
        self,
        config: LauncherConfig,
        theme: Theme | None = None,
    ) -> None:
        self.config = config
        self.theme = theme or Theme()

    def enable_dpi_awareness(self) -> None:
        """
        Improve rendering sharpness on Windows.
        """

        if sys.platform != "win32":
            return

        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                return

    def create_window(
        self,
        *,
        title: str | None = None,
        size: tuple[int, int] | None = None,
        fullscreen: bool = False,
        icon_path: Path | None = None,
    ) -> tk.Tk:
        """
        Create a borderless premium launcher window.
        """

        self.enable_dpi_awareness()

        root = tk.Tk()
        root.title(title or self.config.window_title)
        root.configure(background=self.theme.background)

        if icon_path:
            self.apply_icon(root, icon_path)

        if fullscreen:
            root.attributes("-fullscreen", True)
        else:
            self.center_window(
                root,
                size or self.config.splash_size,
            )

        root.overrideredirect(True)
        root.attributes("-topmost", True)

        return root

    def center_window(
        self,
        root: tk.Tk,
        size: tuple[int, int],
    ) -> None:
        """
        Center a window on the primary display.
        """

        width, height = size
        root.update_idletasks()

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        root.geometry(f"{width}x{height}+{x}+{y}")

    def apply_icon(
        self,
        root: tk.Tk,
        icon_path: Path,
    ) -> None:
        """
        Apply a window icon when supported.
        """

        try:
            root.iconbitmap(str(icon_path))
        except Exception:
            return

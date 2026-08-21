"""
File: core/automation/window_controller.py

Purpose:
Manage desktop windows.

Architecture:

Desktop Agent
        │
WindowController
        │
 Windows API
        │
 Desktop Windows

Future Roadmap
--------------

V1
- Enumerate windows
- Focus windows
- Check existence

V2
- Move windows
- Resize windows
- Minimize / Maximize

V3
- Multi-monitor support
- Window snapshots
- Layout management

V4
- Autonomous desktop orchestration
"""

from __future__ import annotations

from typing import List

import pygetwindow as gw


class WindowController:
    """
    Manage desktop windows.
    """

    def get_window_titles(self) -> List[str]:
        """
        Return all visible window titles.
        """

        titles: List[str] = []

        try:
            for window in gw.getAllWindows():
                title = window.title.strip()

                if title:
                    titles.append(title)

        except Exception:
            pass

        return titles

    def get_window_count(self) -> int:
        """
        Return total visible windows.
        """

        return len(
            self.get_window_titles()
        )

    def window_exists(
        self,
        title: str,
    ) -> bool:
        """
        Check whether a window exists.
        """

        title = title.lower()

        for window_title in self.get_window_titles():

            if title in window_title.lower():
                return True

        return False

    def focus_window(
        self,
        title: str,
    ) -> bool:
        """
        Bring a window to the foreground.

        Returns
        -------
        bool
            True if successful.
        """

        try:

            windows = gw.getWindowsWithTitle(
                title
            )

            if not windows:
                return False

            window = windows[0]

            if window.isMinimized:
                window.restore()

            window.activate()

            return True

        except Exception:
            return False

    def minimize_window(
        self,
        title: str,
    ) -> bool:
        """
        Minimize a window.
        """

        try:

            windows = gw.getWindowsWithTitle(
                title
            )

            if not windows:
                return False

            windows[0].minimize()

            return True

        except Exception:
            return False

    def maximize_window(
        self,
        title: str,
    ) -> bool:
        """
        Maximize a window.
        """

        try:

            windows = gw.getWindowsWithTitle(
                title
            )

            if not windows:
                return False

            windows[0].maximize()

            return True

        except Exception:
            return False

    def close_window(
        self,
        title: str,
    ) -> bool:
        """
        Close a window.
        """

        try:

            windows = gw.getWindowsWithTitle(
                title
            )

            if not windows:
                return False

            windows[0].close()

            return True

        except Exception:
            return False
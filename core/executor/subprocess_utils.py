"""
Shared subprocess options for KAIROS process execution.
"""

from __future__ import annotations

import subprocess
import sys
from typing import Any


def no_window_subprocess_kwargs() -> dict[str, Any]:
    """
    Return subprocess kwargs that prevent extra console windows on Windows.

    Windows creates a new console for console-subsystem children when the
    parent process has no attached console, such as the PySide desktop host.
    Capturing stdout/stderr does not by itself suppress that window.
    """

    if sys.platform != "win32":
        return {}

    return {
        "creationflags": subprocess.CREATE_NO_WINDOW,
    }

"""
Shared launcher utilities.
"""

from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from tkinter import messagebox


@dataclass(frozen=True)
class LauncherConfig:
    """
    Runtime configuration for the launcher startup sequence.
    """

    app_name: str = "KAIROS"
    window_title: str = "KAIROS"
    splash_timeout_ms: int = 2600
    splash_fade_steps: int = 18
    splash_size: tuple[int, int] = (760, 440)
    intro_timeout_ms: int = 15000
    log_name: str = "kairos.launcher"


@dataclass(frozen=True)
class RuntimeEnvironment:
    """
    Paths that differ between development and bundled execution.
    """

    project_root: Path
    executable_dir: Path
    bundled_root: Path | None
    frozen: bool


def get_runtime_environment() -> RuntimeEnvironment:
    """
    Detect development vs PyInstaller execution paths.
    """

    frozen = bool(getattr(sys, "frozen", False))
    bundled_root_value = getattr(sys, "_MEIPASS", None)
    bundled_root = Path(bundled_root_value) if bundled_root_value else None

    if frozen:
        executable_dir = Path(sys.executable).resolve().parent
        project_root = executable_dir
    else:
        executable_dir = Path.cwd().resolve()
        project_root = Path(__file__).resolve().parents[1]

    return RuntimeEnvironment(
        project_root=project_root,
        executable_dir=executable_dir,
        bundled_root=bundled_root,
        frozen=frozen,
    )


def configure_logging(config: LauncherConfig) -> logging.Logger:
    """
    Create a dedicated launcher logger.
    """

    logger = logging.getLogger(config.log_name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    log_dir = Path.cwd() / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    handler = logging.FileHandler(
        log_dir / "launcher.log",
        encoding="utf-8",
    )
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
    )

    logger.addHandler(handler)
    logger.propagate = False

    return logger


def show_error_dialog(
    title: str,
    message: str,
) -> None:
    """
    Show a professional startup error dialog.
    """

    try:
        messagebox.showerror(
            title,
            message,
        )
    except Exception:
        print(f"{title}: {message}", file=sys.stderr)

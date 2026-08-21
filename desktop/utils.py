"""
Shared desktop utilities.
"""

from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DesktopConfig:
    """
    Runtime configuration for the desktop presentation layer.
    """

    app_name: str = "KAIROS"
    organization_name: str = "KAIROS"
    window_title: str = "KAIROS"
    splash_timeout_ms: int = 2600
    splash_fade_ms: int = 420
    intro_timeout_ms: int = 15000
    minimum_window_size: tuple[int, int] = (1080, 700)
    initial_window_size: tuple[int, int] = (1320, 840)
    log_name: str = "kairos.desktop"


@dataclass(frozen=True)
class RuntimeEnvironment:
    """
    Paths that differ between development and PyInstaller execution.
    """

    project_root: Path
    executable_dir: Path
    bundled_root: Path | None
    frozen: bool


def get_runtime_environment() -> RuntimeEnvironment:
    """
    Detect development and PyInstaller execution paths.
    """

    frozen = bool(getattr(sys, "frozen", False))
    bundled_root_value = getattr(sys, "_MEIPASS", None)
    bundled_root = Path(bundled_root_value).resolve() if bundled_root_value else None

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


def configure_logging(config: DesktopConfig) -> logging.Logger:
    """
    Configure desktop-layer file logging.
    """

    logger = logging.getLogger(config.log_name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    log_dir = Path.cwd() / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    handler = logging.FileHandler(
        log_dir / "desktop.log",
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


def format_exception(error: BaseException) -> str:
    """
    Return a concise user-facing exception message.
    """

    return f"{type(error).__name__}: {error}"

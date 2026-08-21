"""
File: core/logging/kairos_logger.py

Purpose:
Central KAIROS logger.

Why:

Provides:

- Clean terminal output
- File logging
- Agent logging
- Debug logging

Architecture:

Agent
  ↓
KairosLogger
  ↓
Terminal + Log File
"""

from pathlib import Path
from datetime import datetime

from core.logging.log_manager import LogManager


class KairosLogger:
    """
    KAIROS Logger.

    Handles terminal output
    and log file writing.
    """

    def __init__(
        self,
        log_name: str = "kairos"
    ):
        """
        Initialize logger.
        """

        self.log_file = (
            LogManager()
            .get_log_file(
                log_name
            )
        )

    def _timestamp(
        self
    ) -> str:
        """
        Generate timestamp.
        """

        return datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def _write(
        self,
        level: str,
        message: str
    ) -> None:
        """
        Write message
        to log file.
        """

        log_entry = (
            f"[{self._timestamp()}] "
            f"[{level}] "
            f"{message}\n"
        )

        Path(
            self.log_file
        ).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.log_file,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                log_entry
            )

    def info(
        self,
        message: str
    ) -> None:
        """
        Information log.
        """

        print(
            f"● {message}"
        )

        self._write(
            "INFO",
            message
        )

    def success(
        self,
        message: str
    ) -> None:
        """
        Success log.
        """

        print(
            f"✓ {message}"
        )

        self._write(
            "SUCCESS",
            message
        )

    def warning(
        self,
        message: str
    ) -> None:
        """
        Warning log.
        """

        print(
            f"⚠ {message}"
        )

        self._write(
            "WARNING",
            message
        )

    def error(
        self,
        message: str
    ) -> None:
        """
        Error log.
        """

        print(
            f"✗ {message}"
        )

        self._write(
            "ERROR",
            message
        )

    def debug(
        self,
        message: str
    ) -> None:
        """
        Debug log.

        Written only
        to log file.
        """

        self._write(
            "DEBUG",
            message
        )
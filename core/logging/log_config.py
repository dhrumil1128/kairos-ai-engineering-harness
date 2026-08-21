"""
File: core/logging/log_config.py

Purpose:
Central logging configuration.

Why:

Provides a single source
of truth for all log files.

Architecture:

KairosLogger
      ↓
LogManager
      ↓
LogConfig
      ↓
logs/
"""

from pathlib import Path


class LogConfig:
    """
    Logging configuration.
    """

    # Root log directory.
    LOG_DIR = (
        Path("logs")
    )

    # Core KAIROS log.
    KAIROS_LOG = (
        LOG_DIR
        / "kairos.log"
    )

    # Agent logs.
    PLANNER_LOG = (
        LOG_DIR
        / "planner.log"
    )

    ARCHITECT_LOG = (
        LOG_DIR
        / "architect.log"
    )


    MEMORY_LOG = (
    LOG_DIR
    / "memory.log"
    )
    
    
    CODER_LOG = (
        LOG_DIR
        / "coder.log"
    )

    REVIEWER_LOG = (
        LOG_DIR
        / "reviewer.log"
    )

    TESTER_LOG = (
        LOG_DIR
        / "tester.log"
    )

    HEALING_LOG = (
        LOG_DIR
        / "healing.log"
    )

    SANDBOX_LOG = (
        LOG_DIR
        / "sandbox.log"
    )
    
    

    @classmethod
    def create_log_directory(
        cls
    ) -> None:
        """
        Create logs directory.
        """

        cls.LOG_DIR.mkdir(
            parents=True,
            exist_ok=True
        )
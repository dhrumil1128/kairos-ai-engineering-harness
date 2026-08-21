"""
File: core/executor/crash_recovery.py

Purpose:
Recover from failed
project execution.

Why:

Provide structured
recovery information
for the recursive
healing system.

Architecture:

Execution Manager
        │
        ▼
Crash Recovery
        │
        ├── Failure Analysis
        ├── Recovery Report
        ├── Recovery Status
        └── Healing
"""

from __future__ import annotations

from core.logging.kairos_logger import (
    KairosLogger
)


class CrashRecovery:
    """
    Enterprise Crash
    Recovery.
    """

    def __init__(
        self
    ):
        """
        Initialize recovery.
        """

        self.logger = (
            KairosLogger(
                "executor"
            )
        )

    # ---------------------------------- #
    # Handle Crash
    # ---------------------------------- #

    def handle(
        self,
        result
    ) -> dict:
        """
        Build recovery
        report.
        """

        self.logger.warning(
            "Crash recovery started."
        )

        report = {

            "success":
            result.success,

            "exit_code":
            result.exit_code,

            "stdout":
            result.stdout,

            "stderr":
            result.stderr,

            "recovery_required":
            (
                not result.success
            )

        }
        
        self.logger.error(
            f"Crash Report:\n{report}"
        )

        self.logger.info(
            "Crash recovery completed."
        )

        return report

    # ---------------------------------- #
    # Recovery Required
    # ---------------------------------- #

    def required(
        self,
        result
    ) -> bool:
        """
        Return recovery
        requirement.
        """

        return (
            not result.success
        )

    # ---------------------------------- #
    # Recovery Summary
    # ---------------------------------- #

    def summary(
        self,
        report: dict
    ) -> dict:
        """
        Return recovery
        summary.
        """

        return {

            "success":
            report[
                "success"
            ],

            "exit_code":
            report[
                "exit_code"
            ],

            "recovery_required":
            report[
                "recovery_required"
            ]

        }
        
        
    
    # ---------------------------------- #
    # Reset Recovery
    # ---------------------------------- #

    def clear(
        self
    ) -> None:
        """
        Reset Crash
        Recovery.
        """

        self.logger.info(
            "Crash Recovery reset."
        )
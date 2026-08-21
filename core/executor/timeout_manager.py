"""
File: core/executor/timeout_manager.py

Purpose:
Prevent execution
from running forever.

Why:

Protects KAIROS from
hung or stalled
executions.

Architecture:

Execution Manager
        │
        ▼
Timeout Manager
        │
        ├── Timeout Check
        ├── Default Timeout
        ├── Timeout Report
        └── Result
"""

from __future__ import annotations

import time

from core.logging.kairos_logger import (
    KairosLogger
)


class TimeoutManager:
    """
    Enterprise Timeout
    Manager.
    """

    def __init__(
        self
    ):
        """
        Initialize manager.
        """

        self.logger = (
            KairosLogger(
                "executor"
            )
        )

        self.timeout = 300

    # ---------------------------------- #
    # Timeout Check
    # ---------------------------------- #

    def expired(
        self,
        start_time: float
    ) -> bool:
        """
        Check whether
        timeout expired.
        """

        return (

            time.time()

            - start_time

            >= self.timeout

        )
        
    
        # ---------------------------------- #
    # Get Timeout
    # ---------------------------------- #

    def get_timeout(
        self
    ) -> int:
        """
        Return configured
        timeout.
        """

        return (
            self.timeout
        )

    # ---------------------------------- #
    # Set Timeout
    # ---------------------------------- #

    def set_timeout(
        self,
        seconds: int
    ) -> None:
        """
        Update timeout.
        """

        self.timeout = (
            seconds
        )

        self.logger.info(
            f"Timeout set to {seconds} seconds."
        )

    # ---------------------------------- #
    # Remaining Time
    # ---------------------------------- #

    def remaining(
        self,
        start_time: float
    ) -> float:
        """
        Return remaining
        execution time.
        """

        return max(

            0,

            self.timeout

            - (
                time.time()
                - start_time
            )

        )
        
    
        # ---------------------------------- #
    # Reset Manager
    # ---------------------------------- #

    def clear(
        self
    ) -> None:
        """
        Reset Timeout
        Manager.
        """

        self.timeout = 300

        self.logger.info(
            "Timeout Manager reset."
        )

    # ---------------------------------- #
    # Timeout Summary
    # ---------------------------------- #

    def summary(
        self
    ) -> dict:
        """
        Return timeout
        configuration.
        """

        return {

            "timeout":
                self.timeout

        }
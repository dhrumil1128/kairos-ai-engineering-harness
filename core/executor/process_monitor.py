"""
File: core/executor/process_monitor.py

Purpose:
Monitor execution
lifecycle.

Why:

Provides real-time
execution monitoring
for reliability and
future recovery.

Architecture:

Execution Manager
        │
        ▼
Process Monitor
        │
        ├── Start
        ├── Stop
        ├── Status
        └── Runtime
"""

from __future__ import annotations

import time

from core.logging.kairos_logger import (
    KairosLogger
)


class ProcessMonitor:
    """
    Enterprise Process
    Monitor.
    """

    def __init__(
        self
    ):
        """
        Initialize monitor.
        """

        self.logger = (
            KairosLogger(
                "executor"
            )
        )

        self.running = False

        self.start_time = None

        self.command = None

    # ---------------------------------- #
    # Start Monitoring
    # ---------------------------------- #

    def start(
        self,
        command: list[str]
    ) -> None:
        """
        Start monitoring
        execution.
        """

        self.command = command

        self.running = True

        self.start_time = (
            time.time()
        )

        self.logger.info(
            "Process monitoring started."
        )
        
    
    
        # ---------------------------------- #
    # Stop Monitoring
    # ---------------------------------- #

    def stop(
        self
    ) -> None:
        """
        Stop monitoring
        execution.
        """

        self.running = False

        self.logger.info(
            "Process monitoring stopped."
        )

    # ---------------------------------- #
    # Runtime
    # ---------------------------------- #

    def runtime(
        self
    ) -> float:
        """
        Return execution
        runtime.
        """

        if self.start_time is None:

            return 0.0

        return (

            time.time()

            - self.start_time

        )

    # ---------------------------------- #
    # Status
    # ---------------------------------- #

    def status(
        self
    ) -> dict:
        """
        Return current
        process status.
        """

        return {

            "running":
            self.running,

            "command":
            self.command,

            "runtime":
            self.runtime()

        }
        
    
    
    # ---------------------------------- #
    # Reset Monitor
    # ---------------------------------- #

    def clear(
        self
    ) -> None:
        """
        Reset Process
        Monitor.
        """

        self.running = False

        self.start_time = None

        self.command = None

        self.logger.info(
            "Process Monitor reset."
        )
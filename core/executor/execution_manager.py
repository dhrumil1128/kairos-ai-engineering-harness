"""
File: core/executor/execution_manager.py

Purpose:
Coordinate reliable
project execution.

Why:

Provide a centralized
execution controller
responsible for running,
monitoring and recovering
project execution.

Architecture:

Execution Pipeline
        │
        ▼
Execution Manager
        │
        ├── Retry Manager
        ├── Timeout Manager
        ├── Process Monitor
        ├── Crash Recovery
        │
        ▼
Sandbox Runner

V2:
- Parallel execution

V3:
- Distributed execution

V4:
- Remote execution

V5:
- Autonomous execution
"""

from __future__ import annotations

from core.logging.kairos_logger import (
    KairosLogger
)

from core.executor.retry_manager import (
    RetryManager
)

from core.executor.timeout_manager import (
    TimeoutManager
)

from core.executor.process_monitor import (
    ProcessMonitor
)

from core.executor.crash_recovery import (
    CrashRecovery
)


class ExecutionManager:
    """
    Enterprise Execution
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

        self.retry = (
            RetryManager()
        )

        self.timeout = (
            TimeoutManager()
        )

        self.monitor = (
            ProcessMonitor()
        )

        self.recovery = (
            CrashRecovery()
        )

    # ---------------------------------- #
    # Execute
    # ---------------------------------- #

    def execute(
        self,
        runner,
        command: list[str],
        working_directory: str
    ):
        """
        Execute using the
        reliability layer.
        """

        self.logger.info(
            "Execution Manager started."
        )
        
        self.monitor.start(
            command
        )

        result = (
            self.retry.execute(

                runner=runner,

                command=command,

                working_directory=(
                    working_directory
                ),

                timeout_manager=(
                    self.timeout
                )

            )
        )

        self.monitor.stop()

        if not result.success:

            self.logger.warning(
                "Execution failed. Starting crash recovery."
            )

            self.recovery.handle(
                result
            )

        self.logger.success(
            "Execution Manager completed."
        )

        return result

    # ---------------------------------- #
    # Health Check
    # ---------------------------------- #

    def healthy(
        self,
        result
    ) -> bool:
        """
        Return execution
        health.
        """

        return result.success
    
        # ---------------------------------- #
    # Execution Summary
    # ---------------------------------- #

    def summary(
        self,
        result
    ) -> dict:
        """
        Return execution
        summary.
        """

        return {

            "success":
            result.success,

            "exit_code":
            result.exit_code,

            "healthy":
            self.healthy(
                result
            )

        }

    # ---------------------------------- #
    # Reset Manager
    # ---------------------------------- #

    def clear(
        self
    ) -> None:
        """
        Reset Execution
        Manager.
        """

        self.logger.info(
            "Execution Manager reset."
        )
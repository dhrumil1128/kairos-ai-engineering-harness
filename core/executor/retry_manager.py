"""
File: core/executor/retry_manager.py

Purpose:
Provide reliable retry
execution for failed
processes.

Why:

Automatically retry
transient execution
failures before handing
control to crash recovery.

Architecture:

Execution Manager
        │
        ▼
Retry Manager
        │
        ├── Retry Loop
        ├── Retry Limit
        ├── Retry Logging
        └── Result
"""

from __future__ import annotations

from core.logging.kairos_logger import (
    KairosLogger
)


class RetryManager:
    """
    Enterprise Retry
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

        self.max_retries = 3

    # ---------------------------------- #
    # Execute With Retry
    # ---------------------------------- #

    def execute(
        self,
        runner,
        command: list[str],
        working_directory: str,
        timeout_manager
    ):
        """
        Execute with
        retry support.
        """

        self.logger.info(
            "Retry Manager started."
        )

        attempt = 0
        
        while (

            attempt
            < self.max_retries

        ):

            attempt += 1

            self.logger.info(
                f"Execution attempt {attempt}"
            )

            result = runner.execute(

                command=command,

                working_directory=(
                    working_directory
                ),

                timeout_manager=(
                    timeout_manager
                )

            )

            if result.success:

                self.logger.success(
                    "Execution succeeded."
                )

                return result

            self.logger.warning(
                f"Attempt {attempt} failed."
            )

        self.logger.error(
            "Retry limit reached."
        )

        return result
    
    # ---------------------------------- #
    # Reset Manager
    # ---------------------------------- #

    def clear(
        self
    ) -> None:
        """
        Reset Retry
        Manager.
        """

        self.logger.info(
            "Retry Manager reset."
        )

    # ---------------------------------- #
    # Retry Count
    # ---------------------------------- #

    def retries(
        self
    ) -> int:
        """
        Return configured
        retry count.
        """

        return (
            self.max_retries
        )
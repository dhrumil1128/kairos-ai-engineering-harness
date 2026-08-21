"""
File: core/executor/execution_pipeline.py

Purpose:
Coordinate the complete
execution reliability
pipeline.

Why:

Provides a single entry
point for reliable
project execution.

Architecture:

Execution Manager
        │
        ▼
Execution Pipeline
        │
        ├── Execute
        ├── Monitor
        ├── Recover
        └── Report
"""

from __future__ import annotations

from core.logging.kairos_logger import (
    KairosLogger
)

from core.executor.execution_manager import (
    ExecutionManager
)


class ExecutionPipeline:
    """
    Enterprise Execution
    Pipeline.
    """

    def __init__(
        self
    ):
        """
        Initialize pipeline.
        """

        self.logger = (
            KairosLogger(
                "executor"
            )
        )

        self.manager = (
            ExecutionManager()
        )

    # ---------------------------------- #
    # Execute Pipeline
    # ---------------------------------- #

    def execute(
        self,
        runner,
        command: list[str],
        working_directory: str
    ):
        """
        Execute the complete
        reliability pipeline.
        """

        self.logger.info(
            "Execution Pipeline started."
        )

        result = (
            self.manager.execute(
                runner=runner,
                command=command,
                working_directory=(
                    working_directory
                )
            )
        )
        
        
        self.logger.success(
            "Execution Pipeline completed."
        )

        return {

            "result":
                result,

            "summary":
                self.manager.summary(
                    result
                ),

            "healthy":
                self.manager.healthy(
                    result
                )

        }

    # ---------------------------------- #
    # Execution Summary
    # ---------------------------------- #

    def summary(
        self,
        execution_result: dict
    ) -> dict:
        """
        Return execution
        summary.
        """

        return (
            execution_result.get(
                "summary",
                {}
            )
        )
        
    
    # ---------------------------------- #
    # Reset Pipeline
    # ---------------------------------- #

    def clear(
        self
    ) -> None:
        """
        Reset Execution
        Pipeline.
        """

        self.manager.clear()

        self.logger.info(
            "Execution Pipeline reset."
        )
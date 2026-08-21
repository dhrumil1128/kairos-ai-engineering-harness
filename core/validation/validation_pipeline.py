"""
File: core/validation/validation_pipeline.py

Purpose:
Coordinate the complete
validation workflow.

Why:

Provides a single entry
point for validating
projects before sandbox
execution.

Architecture:

Validation Manager
        │
        ▼
Validation Pipeline
        │
        ├── Execute Validation
        ├── Build Report
        ├── Build Summary
        │
        ▼
Recursive Healing

V2:
- Parallel Validation

V3:
- Incremental Validation

V4:
- Distributed Validation

V5:
- Autonomous Validation
"""

from __future__ import annotations

from core.logging.kairos_logger import (
    KairosLogger
)

from core.validation.validation_manager import (
    ValidationManager
)

from core.architecture.blueprint import ArchitectureBlueprint

class ValidationPipeline:
    """
    Enterprise Validation
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
                "validation"
            )
        )

        self.manager = (
            ValidationManager()
        )

    # ---------------------------------- #
    # Execute Pipeline
    # ---------------------------------- #

    def execute(
        self,
        project_path: str,
        architecture: ArchitectureBlueprint,
        implementation: dict
    ) -> dict:
        """
        Execute complete
        validation pipeline.
        """

        self.logger.info(
            "Validation Pipeline started."
        )

        report = (
            self.manager.validate(
                project_path,
                architecture,
                implementation
            )
        )
        
        
        self.logger.success(
            "Validation Pipeline completed."
        )

        return {

            "report":
                report,

            "summary":
                self.manager.summary(
                    report
                ),

            "passed":
                self.manager.passed(
                    report
                ),

            "failed_validators":
                self.manager.failed_validators(
                    report
                )

        }

    # ---------------------------------- #
    # Validation Summary
    # ---------------------------------- #

    def summary(
        self,
        validation_result: dict
    ) -> dict:
        """
        Return validation
        summary.
        """

        return (
            validation_result.get(
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
        Reset Validation
        Pipeline.
        """

        self.manager.clear()

        self.logger.info(
            "Validation Pipeline reset."
        )
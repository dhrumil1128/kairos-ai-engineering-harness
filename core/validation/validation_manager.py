"""
File: core/validation/validation_manager.py

Purpose:
Coordinate the complete
validation workflow.

Why:

Before execution, every
generated project should
pass a standardized
validation process.

Architecture:

Project Validator
        │
        ▼
Architecture Validator
        │
        ▼
Code Validator
        │
        ▼
Security Validator
        │
        ▼
Dependency Validator
        │
        ▼
Validation Manager
        │
        ▼
Recursive Healing

V2:
- Parallel validation

V3:
- Incremental validation

V4:
- AI-assisted validation

V5:
- Distributed validation
"""

from __future__ import annotations

from core.logging.kairos_logger import (
    KairosLogger
)

from core.validation.project_validator import (
    ProjectValidator
)

from core.validation.architecture_validator import (
    ArchitectureValidator
)

from core.validation.code_validator import (
    CodeValidator
)

from core.validation.security_validator import (
    SecurityValidator
)

from core.validation.dependency_validator import (
    DependencyValidator
)

from core.architecture.blueprint import ArchitectureBlueprint


class ValidationManager:
    """
    Enterprise Validation
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
                "validation"
            )
        )

        self.project = (
            ProjectValidator()
        )

        self.architecture = (
            ArchitectureValidator()
        )

        self.code = (
            CodeValidator()
        )

        self.security = (
            SecurityValidator()
        )

        self.dependencies = (
            DependencyValidator()
        )

    # ---------------------------------- #
    # Validate Project
    # ---------------------------------- #

    def validate(
        self,
        project_path: str,
        architecture: ArchitectureBlueprint,
        implementation: dict
    ) -> dict:
        """
        Execute complete
        validation workflow.
        """

        self.logger.info(
            "Validation started."
        )

        report = {

            "project":
            self.project.validate(
                project_path
            ),

            "architecture":
            self.architecture.validate(
                architecture
            ),

            "code":
            self.code.validate(
                implementation
            ),

            "security":
            self.security.validate(
                implementation
            ),

            "dependencies":
            self.dependencies.validate(
                project_path
            ),

        }
        
    
        self.logger.success(
            "Validation completed."
        )

        return report

    # ---------------------------------- #
    # Validation Status
    # ---------------------------------- #

    def passed(
        self,
        report: dict
    ) -> bool:
        """
        Return overall
        validation status.
        """

        return all(

            item.get(
                "passed",
                False
            )

            for item
            in report.values()

        )

    # ---------------------------------- #
    # Validation Summary
    # ---------------------------------- #

    def summary(
        self,
        report: dict
    ) -> dict:
        """
        Return validation
        summary.
        """

        passed = 0

        failed = 0

        for result in report.values():

            if result.get(
                "passed",
                False
            ):

                passed += 1

            else:

                failed += 1

        return {

            "passed":
            passed,

            "failed":
            failed,

            "overall":
            self.passed(
                report
            ),

        }
    
    # ---------------------------------- #
    # Failed Validators
    # ---------------------------------- #

    def failed_validators(
        self,
        report: dict
    ) -> list[str]:
        """
        Return failed
        validators.
        """

        failed = []

        for (
            validator,
            result
        ) in report.items():

            if not result.get(
                "passed",
                False
            ):

                failed.append(
                    validator
                )

        return failed

    # ---------------------------------- #
    # Reset Manager
    # ---------------------------------- #

    def clear(
        self
    ) -> None:
        """
        Reset Validation
        Manager.
        """

        self.logger.info(
            "Validation Manager reset."
        )
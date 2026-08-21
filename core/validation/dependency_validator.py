"""
File: core/validation/dependency_validator.py

Purpose:
Validate project
dependencies before
execution.

Why:

Ensures dependency
files exist and are
properly defined.

Architecture:

Project
    │
    ▼
Dependency Validator
    │
    ├── requirements.txt
    ├── pyproject.toml
    ├── setup.py
    └── Report
"""

from __future__ import annotations

from pathlib import Path

from core.logging.kairos_logger import (
    KairosLogger
)


class DependencyValidator:
    """
    Enterprise Dependency
    Validator.
    """

    def __init__(
        self
    ):
        """
        Initialize validator.
        """

        self.logger = (
            KairosLogger(
                "validation"
            )
        )

    # ---------------------------------- #
    # Validate Dependencies
    # ---------------------------------- #

    def validate(
        self,
        project_path: str
    ) -> dict:
        """
        Validate dependency
        files.
        """

        self.logger.info(
            "Dependency validation started."
        )

        project = Path(
            project_path
        )

        report = {

            "passed": True,

            "files": [],

            "errors": []

        }

        dependency_files = [

            "requirements.txt",

            "pyproject.toml",

            "setup.py"

        ]
    
            # ------------------------------
        # Dependency Files
        # ------------------------------

        for file in dependency_files:

            path = (
                project / file
            )

            exists = (
                path.exists()
            )

            report[
                "files"
            ].append(

                {
                    "name":
                    file,

                    "exists":
                    exists
                }

            )

            if not exists:

                report[
                    "errors"
                ].append(

                    f"Missing dependency file: {file}"

                )

        if len(
            report["errors"]
        ) == len(
            dependency_files
        ):

            report[
                "passed"
            ] = False

        self.logger.success(
            "Dependency validation completed."
        )

        return report
    
        # ---------------------------------- #
    # Validation Summary
    # ---------------------------------- #

    def summary(
        self,
        report: dict
    ) -> dict:
        """
        Return dependency
        validation summary.
        """

        return {

            "files":
            len(
                report[
                    "files"
                ]
            ),

            "errors":
            len(
                report[
                    "errors"
                ]
            ),

            "passed":
            report[
                "passed"
            ],

        }

    # ---------------------------------- #
    # Reset Validator
    # ---------------------------------- #

    def clear(
        self
    ) -> None:
        """
        Reset Dependency
        Validator.
        """

        self.logger.info(
            "Dependency Validator reset."
        )
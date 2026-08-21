"""
File: core/validation/project_validator.py

Purpose:
Validate generated
project structure.

Why:

Before execution,
the generated project
must contain all
required files and
directories.

Architecture:

Project
    │
    ▼
Project Validator
    │
    ├── Directory Validation
    ├── File Validation
    ├── Entry Validation
    └── Structure Report
"""

from __future__ import annotations

from pathlib import Path

from core.logging.kairos_logger import (
    KairosLogger
)


class ProjectValidator:
    """
    Enterprise Project
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
    # Validate Project
    # ---------------------------------- #

    def validate(
        self,
        project_path: str
    ) -> dict:
        """
        Validate project
        structure.
        """

        self.logger.info(
            "Project validation started."
        )

        project = Path(
            project_path
        )

        report = {

            "passed": True,

            "directories": [],

            "files": [],

            "errors": []

        }

        required_directories = [

            "src",

            "tests",

            "docs"

        ]

        required_files = [

            "src/main.py"

        ]
        
    # ------------------------------
    # Directories
    # ------------------------------

        for directory in (
            required_directories
        ):

            path = (
                project / directory
            )

            exists = (
                path.exists()
            )

            report[
                "directories"
            ].append(

                {
                    "name":
                    directory,

                    "exists":
                    exists
                }

            )

            if not exists:

                report[
                    "passed"
                ] = False

                report[
                    "errors"
                ].append(

                    f"Missing directory: {directory}"

                )

        # ------------------------------
        # Files
        # ------------------------------

        for file in (
            required_files
        ):

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
                    "passed"
                ] = False

                report[
                    "errors"
                ].append(

                    f"Missing file: {file}"

                )

        self.logger.success(
            "Project validation completed."
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
        Return project
        validation summary.
        """

        return {

            "directories":
            len(
                report[
                    "directories"
                ]
            ),

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
        Reset Project
        Validator.
        """

        self.logger.info(
            "Project Validator reset."
        )
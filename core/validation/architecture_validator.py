"""
File: core/validation/architecture_validator.py

Purpose:
Validate generated
architecture before
implementation.

Why:

Ensures the generated
architecture contains
all required fields and
is internally consistent.

Architecture:

Architecture
      │
      ▼
Architecture Validator
      │
      ├── Schema Validation
      ├── Directory Validation
      ├── File Validation
      └── Report
"""

from __future__ import annotations

from core.logging.kairos_logger import (
    KairosLogger
)

from core.architecture.blueprint import ArchitectureBlueprint

class ArchitectureValidator:
    """
    Enterprise Architecture
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
    # Validate Architecture
    # ---------------------------------- #

    def validate(
        self,
        architecture: ArchitectureBlueprint
    ) -> dict:
        """
        Validate generated
        architecture.
        """

        self.logger.info(
            "Architecture validation started."
        )

        spec = architecture 

        report = {

            "passed": True,

            "errors": []

        }

        required_keys = [

            "project_name",

            "project_type",

            "entry_point",

            "directories",

            "requirements",

            "files"

        ]
        
        # ------------------------------
        # Required Keys
        # ------------------------------

        for key in required_keys:

            if not hasattr(spec, key):

                report[
                    "passed"
                ] = False

                report[
                    "errors"
                ].append(

                    f"Missing key: {key}"

                )

        # ------------------------------
        # Directories
        # ------------------------------

        if not spec.directories:

            report[
                "passed"
            ] = False

            report[
                "errors"
            ].append(
                "No directories defined."
            )

        # ------------------------------
        # Files
        # ------------------------------

        if not spec.files:

            report[
                "passed"
            ] = False

            report[
                "errors"
            ].append(
                "No files defined."
            )

        self.logger.success(
            "Architecture validation completed."
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
        Return architecture
        validation summary.
        """

        return {

            "passed":
            report[
                "passed"
            ],

            "errors":
            len(
                report[
                    "errors"
                ]
            ),

        }

    # ---------------------------------- #
    # Reset Validator
    # ---------------------------------- #

    def clear(
        self
    ) -> None:
        """
        Reset Architecture
        Validator.
        """

        self.logger.info(
            "Architecture Validator reset."
        )

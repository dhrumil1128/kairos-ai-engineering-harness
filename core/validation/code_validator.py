"""
File: core/validation/code_validator.py

Purpose:
Validate generated
implementation code.

Why:

Ensures generated files
contain valid content
before execution.

Architecture:

Implementation
      │
      ▼
Code Validator
      │
      ├── Empty File Check
      ├── Python File Check
      ├── Content Check
      └── Report
"""

from __future__ import annotations

from core.logging.kairos_logger import (
    KairosLogger
)


class CodeValidator:
    """
    Enterprise Code
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
    # Validate Code
    # ---------------------------------- #

    def validate(
        self,
        implementation: dict
    ) -> dict:
        """
        Validate generated
        implementation.
        """

        self.logger.info(
            "Code validation started."
        )

        report = {

            "passed": True,

            "validated_files": 0,

            "errors": []

        }

        files = (
            implementation.get(
                "implementation_spec",
                {}
            ).get(
                "files",
                []
            )
        )
        
                # ------------------------------
        # Validate Files
        # ------------------------------

        for file in files:

            report[
                "validated_files"
            ] += 1

            path = file.get(
                "path",
                ""
            )

            content = file.get(
                "content",
                ""
            )

            if not str(
                content
            ).strip():

                report[
                    "passed"
                ] = False

                report[
                    "errors"
                ].append(

                    f"Empty file: {path}"

                )

            if (

                path.endswith(
                    ".py"
                )

                and

                "import"
                not in content

                and

                "def "
                not in content

                and

                "class "
                not in content

            ):

                report[
                    "errors"
                ].append(

                    f"Suspicious Python file: {path}"

                )

        self.logger.success(
            "Code validation completed."
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
        Return validation
        summary.
        """

        return {

            "validated_files":
            report[
                "validated_files"
            ],

            "errors":
            len(
                report[
                    "errors"
                ]
            ),

            "passed":
            report[
                "passed"
            ]

        }

    # ---------------------------------- #
    # Reset Validator
    # ---------------------------------- #

    def clear(
        self
    ) -> None:
        """
        Reset Code
        Validator.
        """

        self.logger.info(
            "Code Validator reset."
        )
"""
File: core/validation/security_validator.py

Purpose:
Perform basic security
validation on generated
implementation.

Why:

Detect common security
issues before execution.

Architecture:

Implementation
      │
      ▼
Security Validator
      │
      ├── Dangerous Functions
      ├── Hardcoded Secrets
      ├── Shell Execution
      └── Report
"""

from __future__ import annotations

from core.logging.kairos_logger import (
    KairosLogger
)


class SecurityValidator:
    """
    Enterprise Security
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
    # Validate Security
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
            "Security validation started."
        )

        report = {

            "passed": True,

            "warnings": [],

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
        # Security Checks
        # ------------------------------

        dangerous_patterns = [

            "eval(",

            "exec(",

            "os.system(",

            "subprocess.Popen",

            "subprocess.call",

            "subprocess.run(",

            "shell=True",

            "pickle.loads(",

            "marshal.loads("

        ]

        secret_patterns = [

            "API_KEY",

            "SECRET_KEY",

            "PASSWORD",

            "TOKEN",

            "ACCESS_KEY"

        ]

        for file in files:

            path = file.get(
                "path",
                ""
            )

            content = file.get(
                "content",
                ""
            )

            for pattern in dangerous_patterns:

                if pattern in content:

                    report[
                        "passed"
                    ] = False

                    report[
                        "errors"
                    ].append(

                        f"{path}: Dangerous pattern -> {pattern}"

                    )

            for pattern in secret_patterns:

                if pattern in content:

                    report[
                        "warnings"
                    ].append(

                        f"{path}: Possible hardcoded secret -> {pattern}"

                    )

        self.logger.success(
            "Security validation completed."
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
        Return security
        validation summary.
        """

        return {

            "passed":
            report[
                "passed"
            ],

            "warnings":
            len(
                report[
                    "warnings"
                ]
            ),

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
        Reset Security
        Validator.
        """

        self.logger.info(
            "Security Validator reset."
        )
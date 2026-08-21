"""
File: core/healing/error_analyzer.py

Purpose:
Analyze execution failures and
identify likely root causes.

Why:

Before KAIROS can repair a
failure, it must understand:

- What failed
- Why it failed
- How severe it is
- Which agent should respond

Architecture:

Execution
    ↓
Exception
    ↓
Error Analyzer
    ↓
Root Cause Analysis
    ↓
Self Correction
    ↓
Repair Workflow

Future Versions:

V2:
- Advanced pattern matching

V3:
- LLM-assisted analysis

V4:
- Historical error learning

V5:
- Autonomous diagnosis
"""


class ErrorAnalyzer:
    """
    Analyze execution failures.
    """

    def analyze(
        self,
        error_message: str
    ) -> dict:
        """
        Analyze error message and
        classify failure.
        """

        message = (
            error_message.lower()
        )

        # Import failures.
        if (
            "importerror" in message
            or
            "modulenotfounderror" in message
        ):

            return {

                "error_type":
                    "ImportError",

                "root_cause":
                    "Missing dependency or invalid import",

                "severity":
                    "medium",

                "recommended_agent":
                    "CoderAgent"
            }

        # Syntax failures.
        if (
            "syntaxerror" in message
            or
            "invalid syntax" in message
        ):

            return {

                "error_type":
                    "SyntaxError",

                "root_cause":
                    "Invalid Python syntax",

                "severity":
                    "high",

                "recommended_agent":
                    "CoderAgent"
            }

        # Name failures.
        if (
            "nameerror" in message
        ):

            return {

                "error_type":
                    "NameError",

                "root_cause":
                    "Undefined variable or function",

                "severity":
                    "medium",

                "recommended_agent":
                    "CoderAgent"
            }

        # Attribute failures.
        if (
            "attributeerror" in message
        ):

            return {

                "error_type":
                    "AttributeError",

                "root_cause":
                    "Object missing attribute",

                "severity":
                    "medium",

                "recommended_agent":
                    "CoderAgent"
            }

        # Type failures.
        if (
            "typeerror" in message
        ):

            return {

                "error_type":
                    "TypeError",

                "root_cause":
                    "Invalid argument or type mismatch",

                "severity":
                    "medium",

                "recommended_agent":
                    "CoderAgent"
            }

        # File failures.
        if (
            "filenotfounderror" in message
        ):

            return {

                "error_type":
                    "FileNotFoundError",

                "root_cause":
                    "Missing file or invalid path",

                "severity":
                    "medium",

                "recommended_agent":
                    "FilesystemPlugin"
            }

        # Permission failures.
        if (
            "permissionerror" in message
        ):

            return {

                "error_type":
                    "PermissionError",

                "root_cause":
                    "Insufficient permissions",

                "severity":
                    "high",

                "recommended_agent":
                    "SecurityLayer"
            }

        # Runtime failures.
        if (
            "runtimeerror" in message
        ):

            return {

                "error_type":
                    "RuntimeError",

                "root_cause":
                    "Unexpected runtime failure",

                "severity":
                    "high",

                "recommended_agent":
                    "ReviewerAgent"
            }

        # Fallback classification.
        return {

            "error_type":
                "UnknownError",

            "root_cause":
                "Unknown failure",

            "severity":
                "low",

            "recommended_agent":
                "ReviewerAgent"
        }
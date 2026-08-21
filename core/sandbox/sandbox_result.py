"""
File: core/sandbox/sandbox_result.py

Purpose:
Represent sandbox execution
results in a structured way.

Why:

All sandbox executions should
return a consistent result
object regardless of language,
runtime, or execution method.

Architecture:

SandboxExecutor
       ↓
SandboxResult
       ↓
SandboxManager
       ↓
CLIManager

Responsibilities:

- Execution status
- Exit code
- Standard output
- Standard error
- Execution metadata

V1:
- Basic execution results

V2:
- Runtime metrics

V3:
- Resource consumption

V4:
- Container metrics

V5:
- Distributed execution metrics

V6:
- Cloud execution telemetry

V7:
- Autonomous execution analytics

Enterprise:

- Audit metadata
- Compliance tracking
- Security events
- Resource accounting
- Execution traceability
- Governance reporting
"""


class SandboxResult:
    """
    Sandbox execution result.
    """

    def __init__(
        self,
        success: bool,
        exit_code: int,
        stdout: str,
        stderr: str
    ):
        """
        Initialize result.

        Parameters:
            success:
                Execution status.

            exit_code:
                Process exit code.

            stdout:
                Standard output.

            stderr:
                Standard error.
        """

        # Execution status.
        self.success = success

        # Process exit code.
        self.exit_code = exit_code

        # Captured stdout.
        self.stdout = stdout

        # Captured stderr.
        self.stderr = stderr

    def to_dict(
        self
    ) -> dict:
        """
        Convert result
        to dictionary.
        """

        return {
            "success":
                self.success,

            "exit_code":
                self.exit_code,

            "stdout":
                self.stdout,

            "stderr":
                self.stderr
        }

    def has_errors(
        self
    ) -> bool:
        """
        Check whether
        execution failed.
        """

        return (
            not self.success
        )

    def has_output(
        self
    ) -> bool:
        """
        Check whether
        stdout exists.
        """

        return (
            len(
                self.stdout.strip()
            ) > 0
        )

    def has_stderr(
        self
    ) -> bool:
        """
        Check whether
        stderr exists.
        """

        return (
            len(
                self.stderr.strip()
            ) > 0
        )

    def summary(
        self
    ) -> str:
        """
        Generate short
        execution summary.
        """

        if self.success:

            return (
                f"SUCCESS "
                f"(Exit Code: "
                f"{self.exit_code})"
            )

        return (
            f"FAILED "
            f"(Exit Code: "
            f"{self.exit_code})"
        )

    def __repr__(
        self
    ) -> str:
        """
        Debug representation.
        """

        return (
            f"SandboxResult("
            f"success={self.success}, "
            f"exit_code={self.exit_code})"
        )
"""
File: core/sandbox/sandbox_executor.py

Purpose:
Execute generated projects
inside the KAIROS sandbox.

Why:

After project generation,
KAIROS must verify that
the generated code actually
runs successfully.

Architecture:

SandboxManager
       ↓
SandboxExecutor
       ↓
Subprocess
       ↓
SandboxResult

Responsibilities:

- Execute generated code
- Capture stdout
- Capture stderr
- Enforce timeouts
- Return execution results

V1:
- Python execution

V2:
- Test execution

V3:
- Dependency installation

V4:
- Multi-language execution

V5:
- Container execution

V6:
- Distributed execution

V7:
- Autonomous execution environments

Enterprise:

- Docker isolation
- Kubernetes execution
- Resource quotas
- CPU limits
- Memory limits
- Security policies
- Audit logging
- Compliance controls
"""

# Process execution.
import subprocess

# Path utilities.
from pathlib import Path

# Sandbox configuration.
from core.sandbox.sandbox_config import SandboxConfig

# Sandbox result.
from core.sandbox.sandbox_result import SandboxResult

from core.logging.kairos_logger import KairosLogger

from core.sandbox.execution_command_resolver import ExecutionCommandResolver

class SandboxExecutor:
    """
    Execute generated projects.
    """

    def __init__(self):
        """
        Initialize executor.
        """

        self.logger = KairosLogger("sandbox")
        
        self.command_resolver = ExecutionCommandResolver()

    def execute(self, project_path: str) -> SandboxResult:
        """
        Execute project.

        Parameters:
            project_path:
                Generated project.

        Returns:
            SandboxResult
        """

        self.logger.info("Executing Python project")

        self.logger.debug(f"Project Path: {project_path}")

        # Build entrypoint path.
        # Absolute path for validation.
        entrypoint_path = Path(project_path) / SandboxConfig.PYTHON_ENTRYPOINT

        self.logger.debug(f"Entrypoint: {entrypoint_path}")

        # Entrypoint missing.
        if not entrypoint_path.exists():
            return SandboxResult(
                success=False, exit_code=-1, stdout="", stderr=("Entrypoint not found.")
            )

        self.logger.debug(f"type(project_path) = {type(project_path)}")

        self.logger.debug(f"project_path = {project_path}")

        self.logger.debug(
            f"type(PYTHON_ENTRYPOINT) = {type(SandboxConfig.PYTHON_ENTRYPOINT)}"
        )

        self.logger.debug(f"PYTHON_ENTRYPOINT = {SandboxConfig.PYTHON_ENTRYPOINT}")
        
        
        command = self.command_resolver.resolve(
            project_path=project_path
        )
        self.logger.debug(
            f"Command={command}"
        )

        self.logger.debug(
            f"Command Type={type(command)}"
        )

        self.logger.debug(
            f"Command[0] Type={type(command[0])}"
        )

        self.logger.debug(
            f"Command[1] Type={type(command[1])}"
        )

        try:
            # Execute Python file.
            process = subprocess.run(
                command,
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=(SandboxConfig.EXECUTION_TIMEOUT),
            )

            # Successful execution.
            success = process.returncode == 0

            result = SandboxResult(
                success=success,
                exit_code=(process.returncode),
                stdout=(process.stdout),
                stderr=(process.stderr),
            )

            self.logger.debug(f"Exit Code: {process.returncode}")

            self.logger.debug(f"STDOUT:\n{process.stdout}")

            self.logger.debug(f"STDERR:\n{process.stderr}")

            return result

        except subprocess.TimeoutExpired:
            self.logger.error("Execution timeout exceeded")

            return SandboxResult(
                success=False,
                exit_code=-2,
                stdout="",
                stderr=("Execution timeout exceeded."),
            )

        except Exception as error:
            self.logger.error(f"Execution failed: {error}")

            return SandboxResult(
                success=False, exit_code=-3, stdout="", stderr=str(error)
            )

    def execute_tests(self, project_path: str) -> SandboxResult:
        """
        Execute pytest suite.

        Future:
        Used by TesterAgent.
        """

        self.logger.info("Executing test suite")

        try:
            self.logger.debug("Starting subprocess execution")
            process = subprocess.run(
                [SandboxConfig.PYTEST_COMMAND],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=(SandboxConfig.EXECUTION_TIMEOUT),
            )

            return SandboxResult(
                success=(process.returncode == 0),
                exit_code=(process.returncode),
                stdout=(process.stdout),
                stderr=(process.stderr),
            )

        except Exception as error:
            return SandboxResult(
                success=False, exit_code=-1, stdout="", stderr=str(error)
            )

    def install_dependencies(self, project_path: str) -> SandboxResult:
        """
        Future dependency installer.

        V3:
        Automatic dependency
        installation.
        """

        return SandboxResult(
            success=True,
            exit_code=0,
            stdout=("Dependency installation not implemented."),
            stderr="",
        )

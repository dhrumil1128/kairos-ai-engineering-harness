"""
File: core/sandbox/sandbox_manager.py

Purpose:
Manage sandbox lifecycle
and execution flow.

Why:

Generated code should
never execute directly
through the CLI.

Every project must first
pass through a sandbox
layer for validation and
controlled execution.

Architecture:

CLIManager
     ↓
SandboxManager
     ↓
SandboxValidator
     ↓
SandboxExecutor
     ↓
SandboxResult

Responsibilities:

- Manage sandbox execution
- Validate projects
- Execute projects
- Collect results
- Return execution status

V1:
- Basic sandbox management

V2:
- Multi-language execution

V3:
- Resource limits

V4:
- Containerized execution

V5:
- Distributed execution

V6:
- Cloud sandbox execution

V7:
- Autonomous execution environments

Enterprise:

- Docker isolation
- Kubernetes execution
- Resource quotas
- Execution auditing
- Security policies
- Enterprise governance
- Compliance controls
- Distributed sandbox clusters
"""

# Sandbox validation.
from core.sandbox.sandbox_validator import (
    SandboxValidator
)

# Sandbox execution.
from core.sandbox.sandbox_executor import (
    SandboxExecutor
)

# Execution result.
from core.sandbox.sandbox_result import (
    SandboxResult
)

from core.logging.kairos_logger import KairosLogger

class SandboxManager:
    """
    Manage sandbox lifecycle.
    """

    def __init__(
        self
    ):
        """
        Initialize sandbox manager.
        """

        # Create validator.
        self.validator = (
            SandboxValidator()
        )

        # Create executor.
        self.executor = (
            SandboxExecutor()
        )
        
        
        
        # Sandbox logger.
        self.logger = KairosLogger(
            "sandbox"
        )


    def execute_project(
        self,
        project_path: str
    ) -> SandboxResult:
        """
        Execute generated project.

        Parameters:
            project_path:
                Generated project path.

        Returns:
            SandboxResult
        """

      


        self.logger.info(
    "Sandbox validation started"
)
        
        
        
        # Validate project.
        validation_result = (
            self.validator.validate(
                project_path
            )
        )

        # Validation failed.
        if not validation_result:

           

            self.logger.error(
    "Sandbox validation failed"
)
            
            
            
            return SandboxResult(
                success=False,
                exit_code=-1,
                stdout="",
                stderr=(
                    "Sandbox validation failed."
                )
            )

        self.logger.success(
            "Sandbox validation passed"
        )

        self.logger.info(
            "Sandbox execution started"
        )

        # Execute project.
        result = (
            self.executor.execute(
                project_path
            )
        )

        self.logger.debug(
    f"Execution Result:\n{result}"
        )

        if result.success:

            self.logger.success(
                "Sandbox execution completed"
            )

        else:

            self.logger.error(
                "Sandbox execution failed"
            )

        return result
    
    
    

    def validate_project(
        self,
        project_path: str
    ) -> bool:
        """
        Validate project only.

        Parameters:
            project_path:
                Project location.

        Returns:
            Validation status.
        """

        return (
            self.validator.validate(
                project_path
            )
        )

    def get_status(
        self
    ) -> dict:
        """
        Return sandbox status.

        Returns:
            Sandbox metadata.
        """

        return {
            "status": "active",
            "validator":
                self.validator.__class__.__name__,
            "executor":
                self.executor.__class__.__name__
        }
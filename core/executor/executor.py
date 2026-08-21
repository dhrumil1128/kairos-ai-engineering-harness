"""
File: core/executor/executor.py

Purpose:
Primary execution layer for KAIROS.

Responsibilities:

- Execute tasks
- Delegate command execution
- Return execution results

Architecture:

Task
 ↓
Executor
 ↓
CommandRunner
 ↓
Operating System

Version 2:

Now integrates with CommandRunner
instead of returning hardcoded success.
"""

# Shared task contract used across KAIROS.
from core.shared.schemas import TaskSchema

# Real command execution layer.
from core.executor.command_runner import CommandRunner


# Glasswing Security Shield.
# Validates commands before execution.
from core.security.security_guard import SecurityGuard



# Stores execution records for
# auditing and debugging.
from core.executor.execution_history import (
    ExecutionHistory
)
class Executor:
    """
    Core execution service.

    Responsibilities:

    - Receive tasks
    - Translate tasks into commands
    - Execute commands
    - Return results

    Future:

    - Sandbox execution
    - MCP execution
    - Docker execution
    - Cloud execution
    """

    def __init__(self):
        """
        Initialize execution dependencies.
        """

        # Dedicated command execution layer.
        self.command_runner = CommandRunner()
        
        
        # First security layer.
        # Every command must be validated
        # before reaching the operating system.
        self.security_guard = SecurityGuard()
        
        
        
        # Execution tracking layer.
        self.execution_history = (
            ExecutionHistory()
        )

    def execute(self, task: TaskSchema) -> bool:
        """
        Execute a task.

        Parameters:
            task:
                Task to execute.

        Returns:
            bool:
                True if execution succeeds.
                False otherwise.
        """

        # Version 2 command.
        #
        # Later this will come from:
        # Planner → Task → Executor
        #
        # For now we use a safe command
        # to validate the execution pipeline.
        command = "echo KAIROS_EXECUTION"

        # Validate command through
        # Glasswing Security Shield.
        security_result = (
            self.security_guard.validate_command(
                command
            )
        )

        # Stop execution immediately
        # if command is blocked.
        if not security_result["allowed"]:
            return False

        # Execute approved command.
        result = self.command_runner.run(command)

        # Record execution event.
        self.execution_history.add_record(
            task_id=task.id,
            command=command,
            success=result["success"],
            return_code=result["return_code"],
        )

        return result["success"]
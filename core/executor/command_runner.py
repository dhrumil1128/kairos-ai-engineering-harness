"""
File: core/executor/command_runner.py

Purpose:
Execute operating system commands and return
structured execution results.

Why this file exists:

The Executor should not directly interact with
the operating system.

Instead:

Executor
    ↓
CommandRunner
    ↓
Operating System

This keeps responsibilities separated and makes
future sandbox integration easier.

Version 1 Features:

- Execute commands
- Capture stdout
- Capture stderr
- Capture return code

Future Features:

- Sandbox integration
- Command allowlists
- Security validation
- Resource limits
- Execution history
"""

# Used to execute operating system commands.
import subprocess

# Used for type annotations.
from typing import Dict, Any


class CommandRunner:
    """
    Executes system commands and captures results.

    Future:
    All commands will pass through the
    Glasswing Security Layer before execution.
    """

    def run(self, command: str) -> Dict[str, Any]:
        """
        Execute a command and return structured output.

        Parameters:
            command:
                Operating system command to execute.

        Returns:
            Dict[str, Any]

            Example:

            {
                "success": True,
                "stdout": "...",
                "stderr": "...",
                "return_code": 0
            }
        """

        try:

            # Execute command and capture output.
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )

            return {
                "success": result.returncode == 0,

                # Standard command output.
                "stdout": result.stdout,

                # Error output.
                "stderr": result.stderr,

                # Exit code returned by OS.
                "return_code": result.returncode
            }

        except Exception as error:

            return {
                "success": False,
                "stdout": "",
                "stderr": str(error),
                "return_code": -1
            }
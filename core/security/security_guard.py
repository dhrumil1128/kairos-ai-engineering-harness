"""
File: core/security/security_guard.py

Purpose:
Glasswing Security Shield V1.

Responsibilities:

- Validate commands before execution
- Block dangerous operations
- Provide security decisions
- Serve as the first security layer
  before command execution

Architecture:

Task
 ↓
Recursive Engine
 ↓
Executor
 ↓
Security Guard
 ↓
Command Runner
 ↓
Operating System

Future Versions:

V2:
- Risk Scoring Engine

V3:
- Secret Detection

V4:
- Filesystem Policies

V5:
- Enterprise Policy Engine
"""

# Used for command pattern matching.
import re

# Used for structured typing.
from typing import Dict, Any


class SecurityGuard:
    """
    Glasswing Security Shield V1.

    Validates commands before they reach
    the operating system.
    """

    # Commands that are considered dangerous.
    #
    # NOTE:
    # This list will expand significantly
    # in future versions.
    BLOCKED_PATTERNS = [
        r"rm\s+-rf",
        r"shutdown",
        r"reboot",
        r"format",
        r"del\s+/f",
        r"Remove-Item",
        r"mkfs",
    ]

    def validate_command(self, command: str) -> Dict[str, Any]:
        """
        Validate whether a command is allowed.

        Parameters:
            command:
                Command to validate.

        Returns:

            {
                "allowed": bool,
                "reason": str
            }
        """

        # Normalize command for comparison.
        normalized_command = command.lower()

        # Check against all blocked patterns.
        for pattern in self.BLOCKED_PATTERNS:

            if re.search(
                pattern,
                normalized_command,
                re.IGNORECASE
            ):
                return {
                    "allowed": False,
                    "reason": (
                        "Dangerous command "
                        "detected."
                    )
                }

        # Command is considered safe.
        return {
            "allowed": True,
            "reason": "Command approved."
        }
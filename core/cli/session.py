"""
File: core/cli/session.py

Purpose:
Manage interactive CLI sessions.

Why:

Provides a persistent
interactive experience.

Architecture:

Session
 ↓
Prompt
 ↓
CLI Manager
 ↓
Response
"""

from core.cli.prompt import (
    Prompt
)

from core.cli.cli_manager import (
    CLIManager
)


class Session:
    """
    Interactive CLI session.
    """

    def __init__(self):
        """
        Initialize session.
        """

        # User prompt.
        self.prompt = Prompt()

        # Command processor.
        self.manager = CLIManager()

        # Session state.
        self.active = True

    def stop(self):
        """
        Stop session.
        """

        self.active = False

    def is_active(self) -> bool:
        """
        Return session state.
        """

        return self.active

    def process_command(
        self,
        command: str
    ) -> dict:
        """
        Process command.
        """

        if command.lower() in (
            "exit",
            "quit"
        ):
            self.stop()

            return {
                "status": "exit"
            }

        return (
            self.manager
            .process_command(
                command
            )
        )
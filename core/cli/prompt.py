"""
File: core/cli/prompt.py

Purpose:
Handle CLI user input.

Why:

Provides a consistent
prompt experience.

Supports both:

- Single-line commands
- Multi-line AI prompts

Architecture:

CLI
 ↓
Prompt
 ↓
User Command
"""


class Prompt:
    """
    CLI prompt manager.
    """

    def __init__(self):
        """
        Initialize prompt.
        """

        self.prompt_text = (
            "kairos > "
        )

        self.continuation_prompt = (
            "> "
        )

    # ----------------------------------
    # Get Prompt
    # ----------------------------------

    def get_prompt(
        self
    ) -> str:
        """
        Return prompt text.
        """

        return self.prompt_text

    # ----------------------------------
    # Get User Input
    # ----------------------------------

    def get_input(
        self
    ) -> str:
        """
        Read user input.

        Supports:

        • Single-line commands

        • Multi-line prompts.

        Multi-line mode ends
        when the user types:

        /end
        """

        first_line = input(
            self.prompt_text
        )

        # Empty command.
        if not first_line.strip():

            return ""

        # Built-in commands remain
        # single-line commands.
        if first_line.startswith("/"):

            return first_line

        # Exit commands remain
        # single-line.
        if first_line.lower() in (
            "exit",
            "quit"
        ):

            return first_line

        # Collect multiple lines.
        lines = [
            first_line
        ]

        while True:

            line = input(
                self.continuation_prompt
            )

            if (
                line.strip().lower()
                == "/end"
            ):
                break

            lines.append(
                line
            )

        return "\n".join(
            lines
        )
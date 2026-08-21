"""
File: core/tools/terminal_tool.py

Purpose:
Execute terminal commands.

Examples:

- pytest
- git status
- python app.py

Future Versions:

V2:
- Timeout support

V3:
- Command history

V4:
- Streaming output

V5:
- Secure sandbox execution
"""

import subprocess


class TerminalTool:
    """
    Terminal execution tool.
    """

    def run(
        self,
        command: str
    ) -> str:
        """
        Execute command.
        """

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        return (
            result.stdout
            + result.stderr
        )
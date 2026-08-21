"""
File: core/plugins/terminal_plugin.py

Purpose:
Terminal plugin for KAIROS.

Uses TerminalTool to execute
commands.

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

from core.plugins.plugin_base import (
    PluginBase
)

from core.tools.terminal_tool import (
    TerminalTool
)


class TerminalPlugin(
    PluginBase
):
    """
    Terminal plugin.
    """

    def __init__(self):
        """
        Initialize plugin.
        """

        super().__init__(
            name="TerminalPlugin"
        )

        self.terminal_tool = (
            TerminalTool()
        )

    def execute(
        self,
        command: str
    ) -> str:
        """
        Execute command.
        """

        return (
            self.terminal_tool
            .run(command)
        )
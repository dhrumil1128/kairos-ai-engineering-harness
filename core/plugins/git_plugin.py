"""
File: core/plugins/git_plugin.py

Purpose:
Git plugin for KAIROS.

Uses GitTool to perform
repository operations.

Future Versions:

V2:
- Commit support

V3:
- Branch management

V4:
- Pull request support

V5:
- Repository automation
"""

from core.plugins.plugin_base import (
    PluginBase
)

from core.tools.git_tool import (
    GitTool
)


class GitPlugin(
    PluginBase
):
    """
    Git plugin.
    """

    def __init__(self):
        """
        Initialize plugin.
        """

        super().__init__(
            name="GitPlugin"
        )

        self.git_tool = GitTool()

    def execute(
        self,
        action: str
    ):
        """
        Execute git action.
        """

        if action == "status":
            return (
                self.git_tool
                .status()
            )

        if action == "branch":
            return (
                self.git_tool
                .current_branch()
            )

        raise ValueError(
            f"Unknown action: {action}"
        )
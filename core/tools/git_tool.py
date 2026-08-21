"""
File: core/tools/git_tool.py

Purpose:
Git operations for KAIROS.

Examples:

- git status
- git branch
- git diff

Future Versions:

V2:
- Commit support

V3:
- Branch creation

V4:
- Pull request support

V5:
- Repository automation
"""

import subprocess


class GitTool:
    """
    Git operations tool.
    """

    def status(self) -> str:
        """
        Get repository status.
        """

        result = subprocess.run(
            "git status --short",
            shell=True,
            capture_output=True,
            text=True
        )

        return (
            result.stdout
            + result.stderr
        )

    def current_branch(self) -> str:
        """
        Get current branch.
        """

        result = subprocess.run(
            "git branch --show-current",
            shell=True,
            capture_output=True,
            text=True
        )

        return result.stdout.strip()
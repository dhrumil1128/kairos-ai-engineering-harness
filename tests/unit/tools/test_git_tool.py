"""
File:
tests/unit/tools/
test_git_tool.py

Purpose:
Unit tests for GitTool.
"""

from core.tools.git_tool import (
    GitTool
)


def test_git_tool_creation():
    """
    Verify creation.
    """

    tool = GitTool()

    assert tool is not None


def test_status_returns_string():
    """
    Verify status output.
    """

    tool = GitTool()

    result = tool.status()

    assert isinstance(
        result,
        str
    )


def test_branch_returns_string():
    """
    Verify branch output.
    """

    tool = GitTool()

    result = tool.current_branch()

    assert isinstance(
        result,
        str
    )
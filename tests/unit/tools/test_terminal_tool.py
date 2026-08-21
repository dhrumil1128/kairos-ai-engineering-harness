"""
File:
tests/unit/tools/
test_terminal_tool.py

Purpose:
Unit tests for TerminalTool.
"""

from core.tools.terminal_tool import (
    TerminalTool
)


def test_terminal_creation():
    """
    Verify creation.
    """

    tool = TerminalTool()

    assert tool is not None


def test_run_echo_command():
    """
    Verify command execution.
    """

    tool = TerminalTool()

    result = tool.run(
        "echo KAIROS_OK"
    )

    assert (
        "KAIROS_OK"
        in result
    )


def test_run_python_version():
    """
    Verify python access.
    """

    tool = TerminalTool()

    result = tool.run(
        "python --version"
    )

    assert (
        "Python"
        in result
    )
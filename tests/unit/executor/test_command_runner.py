"""
File: tests/unit/executor/test_command_runner.py

Purpose:
Unit tests for CommandRunner.

Why:
Verify command execution and output capture.

Architecture:

Executor
    ↓
CommandRunner
    ↓
Operating System
"""

# Command execution layer under test.
from core.executor.command_runner import CommandRunner


def test_command_runner_creation():
    """
    Verify runner initialization.
    """

    runner = CommandRunner()

    assert runner is not None


def test_echo_command():
    """
    Verify command execution works.
    """

    runner = CommandRunner()

    result = runner.run("echo hello")

    assert result["success"] is True
    assert result["return_code"] == 0


def test_invalid_command():
    """
    Verify invalid commands fail gracefully.
    """

    runner = CommandRunner()

    result = runner.run("this_command_does_not_exist")

    assert result["success"] is False
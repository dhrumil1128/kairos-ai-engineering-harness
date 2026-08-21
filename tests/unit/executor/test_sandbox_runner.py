"""
File: tests/unit/executor/test_sandbox_runner.py

Purpose:
Unit tests for SandboxRunner.

Why:
Verify workspace creation and sandbox execution.

Architecture:

Executor
    ↓
Sandbox Runner
    ↓
Command Runner
"""

# Sandbox layer under test.
from core.executor.sandbox_runner import SandboxRunner

# Filesystem path support.
from pathlib import Path


def test_sandbox_creation():
    """
    Verify sandbox runner initialization.
    """

    sandbox = SandboxRunner()

    assert sandbox is not None


def test_workspace_creation():
    """
    Verify isolated workspace creation.
    """

    sandbox = SandboxRunner()

    workspace = sandbox.create_workspace()

    assert isinstance(workspace, Path)
    assert workspace.exists()


def test_command_execution():
    """
    Verify command execution inside sandbox.
    """

    sandbox = SandboxRunner()

    result = sandbox.execute("echo hello")

    assert result["success"] is True
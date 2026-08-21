"""
File:
tests/unit/runtime/test_runtime_manager.py

Purpose:
Verify runtime setup.
"""

from core.runtime.runtime_manager import (
    RuntimeManager
)


def test_runtime_creation():
    """
    Verify creation.
    """

    runtime = RuntimeManager()

    assert runtime is not None


def test_mcp_server_exists():
    """
    Verify MCP server.
    """

    runtime = RuntimeManager()

    assert (
        runtime.mcp_server
        is not None
    )


def test_plugin_manager_exists():
    """
    Verify plugin manager.
    """

    runtime = RuntimeManager()

    assert (
        runtime.plugin_manager
        is not None
    )


def test_initialize():
    """
    Verify initialization.
    """

    runtime = RuntimeManager()

    runtime.initialize()

    assert True
"""
File:
tests/unit/plugins/
test_terminal_plugin.py

Purpose:
Verify TerminalPlugin.
"""

from core.plugins.terminal_plugin import (
    TerminalPlugin
)


def test_plugin_name():
    """
    Verify plugin name.
    """

    plugin = TerminalPlugin()

    assert (
        plugin.name
        == "TerminalPlugin"
    )


def test_execute_echo():
    """
    Verify execution.
    """

    plugin = TerminalPlugin()

    result = plugin.execute(
        "echo KAIROS_PLUGIN_OK"
    )

    assert (
        "KAIROS_PLUGIN_OK"
        in result
    )


def test_execute_python_version():
    """
    Verify python access.
    """

    plugin = TerminalPlugin()

    result = plugin.execute(
        "python --version"
    )

    assert (
        "Python"
        in result
    )
"""
File:
tests/unit/plugins/
test_browser_plugin.py

Purpose:
Verify BrowserPlugin.
"""

from core.plugins.browser_plugin import (
    BrowserPlugin
)


def test_plugin_name():
    """
    Verify plugin name.
    """

    plugin = BrowserPlugin()

    assert (
        plugin.name
        == "BrowserPlugin"
    )


def test_execute():
    """
    Verify execution.
    """

    plugin = BrowserPlugin()

    result = plugin.execute(
        "https://example.com"
    )

    assert (
        result
        == "Opened: https://example.com"
    )


def test_execute_returns_string():
    """
    Verify output type.
    """

    plugin = BrowserPlugin()

    result = plugin.execute(
        "https://kairos.ai"
    )

    assert isinstance(
        result,
        str
    )
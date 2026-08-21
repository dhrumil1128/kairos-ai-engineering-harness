"""
File:
tests/unit/plugins/
test_security_plugin.py

Purpose:
Verify SecurityPlugin.
"""

from core.plugins.security_plugin import (
    SecurityPlugin
)


def test_plugin_name():
    """
    Verify plugin name.
    """

    plugin = SecurityPlugin()

    assert (
        plugin.name
        == "SecurityPlugin"
    )


def test_detect_password():
    """
    Verify password detection.
    """

    plugin = SecurityPlugin()

    result = plugin.execute(
        "my password is 123"
    )

    assert (
        "Potential password detected."
        in result
    )


def test_detect_secret():
    """
    Verify secret detection.
    """

    plugin = SecurityPlugin()

    result = plugin.execute(
        "this contains secret data"
    )

    assert (
        "Potential secret detected."
        in result
    )


def test_no_findings():
    """
    Verify clean content.
    """

    plugin = SecurityPlugin()

    result = plugin.execute(
        "hello world"
    )

    assert result == []
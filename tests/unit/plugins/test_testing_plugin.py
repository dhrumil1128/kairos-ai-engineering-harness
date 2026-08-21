"""
File:
tests/unit/plugins/
test_testing_plugin.py

Purpose:
Verify TestingPlugin.
"""

from core.plugins.testing_plugin import (
    TestingPlugin
)


def test_plugin_name():
    """
    Verify plugin name.
    """

    plugin = TestingPlugin()

    assert (
        plugin.name
        == "TestingPlugin"
    )


def test_detect_passed():
    """
    Verify pass detection.
    """

    plugin = TestingPlugin()

    result = plugin.execute(
        "10 passed in 1.2s"
    )

    assert (
        result["passed"]
        is True
    )


def test_detect_failed():
    """
    Verify failure detection.
    """

    plugin = TestingPlugin()

    result = plugin.execute(
        "2 failed, 8 passed"
    )

    assert (
        result["failed"]
        is True
    )


def test_clean_result():
    """
    Verify output structure.
    """

    plugin = TestingPlugin()

    result = plugin.execute(
        "all good"
    )

    assert isinstance(
        result,
        dict
    )
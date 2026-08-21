"""
File:
tests/unit/plugins/
test_plugin_base.py

Purpose:
Verify PluginBase.
"""

import pytest

from core.plugins.plugin_base import (
    PluginBase
)


class MockPlugin(
    PluginBase
):
    """
    Test plugin.
    """

    def __init__(self):
        super().__init__(
            name="MockPlugin"
        )

    def execute(
        self
    ):
        return "OK"


def test_plugin_creation():
    """
    Verify creation.
    """

    plugin = MockPlugin()

    assert (
        plugin.name
        == "MockPlugin"
    )


def test_plugin_execute():
    """
    Verify execution.
    """

    plugin = MockPlugin()

    assert (
        plugin.execute()
        == "OK"
    )


def test_base_plugin_execute_error():
    """
    Verify abstract behavior.
    """

    plugin = PluginBase(
        name="BasePlugin"
    )

    with pytest.raises(
        NotImplementedError
    ):
        plugin.execute()
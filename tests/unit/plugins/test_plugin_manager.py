"""
File:
tests/unit/plugins/
test_plugin_manager.py

Purpose:
Verify plugin manager.
"""

from core.plugins.plugin_manager import (
    PluginManager
)


def test_manager_creation():
    """
    Verify creation.
    """

    manager = PluginManager()

    assert manager is not None


def test_register_plugin():
    """
    Verify registration.
    """

    manager = PluginManager()

    plugin = object()

    manager.register_plugin(
        "test_plugin",
        plugin
    )

    assert (
        manager.has_plugin(
            "test_plugin"
        )
        is True
    )


def test_get_plugin():
    """
    Verify retrieval.
    """

    manager = PluginManager()

    plugin = object()

    manager.register_plugin(
        "test_plugin",
        plugin
    )

    assert (
        manager.get_plugin(
            "test_plugin"
        )
        is plugin
    )


def test_list_plugins():
    """
    Verify listing.
    """

    manager = PluginManager()

    manager.register_plugin(
        "plugin_a",
        object()
    )

    manager.register_plugin(
        "plugin_b",
        object()
    )

    assert (
        len(
            manager.list_plugins()
        )
        == 2
    )
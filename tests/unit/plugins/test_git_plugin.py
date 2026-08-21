"""
File:
tests/unit/plugins/
test_git_plugin.py

Purpose:
Verify GitPlugin.
"""

import pytest

from core.plugins.git_plugin import (
    GitPlugin
)


def test_plugin_name():
    """
    Verify plugin name.
    """

    plugin = GitPlugin()

    assert (
        plugin.name
        == "GitPlugin"
    )


def test_status_returns_string():
    """
    Verify status action.
    """

    plugin = GitPlugin()

    result = plugin.execute(
        "status"
    )

    assert isinstance(
        result,
        str
    )


def test_branch_returns_string():
    """
    Verify branch action.
    """

    plugin = GitPlugin()

    result = plugin.execute(
        "branch"
    )

    assert isinstance(
        result,
        str
    )


def test_invalid_action():
    """
    Verify validation.
    """

    plugin = GitPlugin()

    with pytest.raises(
        ValueError
    ):
        plugin.execute(
            "invalid"
        )
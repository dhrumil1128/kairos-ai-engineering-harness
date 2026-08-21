"""
File:
tests/unit/automation/
test_window_controller.py

Purpose:
Verify real window controller.
"""

from core.automation.window_controller import (
    WindowController
)


def test_controller_creation():
    """
    Verify creation.
    """

    controller = (
        WindowController()
    )

    assert (
        controller
        is not None
    )


def test_window_titles():
    """
    Verify title retrieval.
    """

    controller = (
        WindowController()
    )

    titles = (
        controller.get_window_titles()
    )

    assert isinstance(
        titles,
        list
    )


def test_window_count():
    """
    Verify count retrieval.
    """

    controller = (
        WindowController()
    )

    count = (
        controller.get_window_count()
    )

    assert (
        count >= 0
    )


def test_window_exists_returns_bool():
    """
    Verify existence check.
    """

    controller = (
        WindowController()
    )

    result = (
        controller.window_exists(
            "Chrome"
        )
    )

    assert isinstance(
        result,
        bool
    )
    

def test_focus_window_exists():

    controller = (
        WindowController()
    )

    assert hasattr(
        controller,
        "focus_window"
    )
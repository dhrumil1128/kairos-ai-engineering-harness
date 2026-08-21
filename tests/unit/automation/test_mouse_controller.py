"""
File:
tests/unit/automation/
test_mouse_controller.py

Purpose:
Verify mouse controller.
"""

from core.automation.mouse_controller import (
    MouseController
)


def test_controller_creation():
    """
    Verify creation.
    """

    controller = (
        MouseController()
    )

    assert (
        controller
        is not None
    )


def test_position():
    """
    Verify position retrieval.
    """

    controller = (
        MouseController()
    )

    position = (
        controller.get_position()
    )

    assert isinstance(
        position,
        tuple
    )


def test_click():
    """
    Verify click action.
    """

    controller = (
        MouseController()
    )

    result = controller.click()

    assert (
        result
        == "Click approved"
    )


def test_position_length():
    """
    Verify coordinate count.
    """

    controller = (
        MouseController()
    )

    position = (
        controller.get_position()
    )

    assert (
        len(position)
        == 2
    )


def test_move_mouse_exists():

    controller = (
        MouseController()
    )

    assert hasattr(
        controller,
        "move_mouse"
    )


def test_click_exists():

    controller = (
        MouseController()
    )

    assert hasattr(
        controller,
        "click"
    )


def test_double_click_exists():

    controller = (
        MouseController()
    )

    assert hasattr(
        controller,
        "double_click"
    )
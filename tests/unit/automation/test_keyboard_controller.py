"""
File:
tests/unit/automation/
test_keyboard_controller.py

Purpose:
Verify keyboard controller.
"""

from core.automation.keyboard_controller import (
    KeyboardController
)


def test_controller_creation():
    """
    Verify creation.
    """

    controller = (
        KeyboardController()
    )

    assert (
        controller
        is not None
    )


def test_type_text():
    """
    Verify typing.
    """

    controller = (
        KeyboardController()
    )

    result = controller.type_text(
        "KAIROS"
    )

    assert (
        result
        == "Typed: KAIROS"
    )


def test_press_key():
    """
    Verify key press.
    """

    controller = (
        KeyboardController()
    )

    result = controller.press_key(
        "enter"
    )

    assert (
        result
        == "Pressed: enter"
    )


def test_return_types():
    """
    Verify return types.
    """

    controller = (
        KeyboardController()
    )

    assert isinstance(
        controller.type_text(
            "test"
        ),
        str
    )
    

def test_type_text_exists():

    controller = (
        KeyboardController()
    )

    assert hasattr(
        controller,
        "type_text"
    )


def test_press_key_exists():

    controller = (
        KeyboardController()
    )

    assert hasattr(
        controller,
        "press_key"
    )
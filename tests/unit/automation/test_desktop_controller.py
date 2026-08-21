"""
File:
tests/unit/automation/
test_desktop_controller.py

Purpose:
Verify desktop controller.
"""

from core.automation.desktop_controller import (
    DesktopController
)


def test_controller_creation():
    """
    Verify creation.
    """

    controller = (
        DesktopController()
    )

    assert (
        controller
        is not None
    )


def test_status():
    """
    Verify status.
    """

    controller = (
        DesktopController()
    )

    status = (
        controller.get_status()
    )

    assert isinstance(
        status,
        dict
    )


def test_status_keys():
    """
    Verify components.
    """

    controller = (
        DesktopController()
    )

    status = (
        controller.get_status()
    )

    assert (
        "applications"
        in status
    )


def test_all_enabled():
    """
    Verify controllers loaded.
    """

    controller = (
        DesktopController()
    )

    status = (
        controller.get_status()
    )

    assert all(
        status.values()
    )
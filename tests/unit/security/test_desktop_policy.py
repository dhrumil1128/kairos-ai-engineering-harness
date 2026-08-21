"""
File:
tests/unit/security/
test_desktop_policy.py

Purpose:
Verify desktop policy.
"""

from core.security.desktop_policy import (
    DesktopPolicy
)


def test_policy_creation():
    """
    Verify policy creation.
    """

    policy = DesktopPolicy()

    assert (
        policy
        is not None
    )


def test_allowed_application():
    """
    Verify allowed app.
    """

    policy = DesktopPolicy()

    assert (
        policy.is_allowed(
            "Code"
        )
        is True
    )


def test_blocked_application():
    """
    Verify blocked app.
    """

    policy = DesktopPolicy()

    assert (
        policy.is_allowed(
            "Notepad"
        )
        is False
    )


def test_allowed_list():
    """
    Verify allowed list.
    """

    policy = DesktopPolicy()

    apps = (
        policy.get_allowed_apps()
    )

    assert (
        len(apps)
        > 0
    )
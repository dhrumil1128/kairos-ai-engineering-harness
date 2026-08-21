"""
File:
tests/unit/cli/test_session.py

Purpose:
Verify CLI session.
"""

from core.cli.session import (
    Session
)


def test_session_creation():
    """
    Verify creation.
    """

    session = Session()

    assert session is not None


def test_session_active():
    """
    Verify active state.
    """

    session = Session()

    assert (
        session.is_active()
        is True
    )


def test_session_stop():
    """
    Verify stop.
    """

    session = Session()

    session.stop()

    assert (
        session.is_active()
        is False
    )


def test_exit_command():
    """
    Verify exit handling.
    """

    session = Session()

    result = (
        session.process_command(
            "exit"
        )
    )

    assert (
        result["status"]
        == "exit"
    )
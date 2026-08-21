"""
File:
tests/unit/cli/test_startup.py

Purpose:
Verify startup checks.
"""

from core.cli.startup import (
    Startup
)


def test_startup_creation():
    """
    Verify creation.
    """

    startup = Startup()

    assert startup is not None


def test_startup_checks_exist():
    """
    Verify checks exist.
    """

    startup = Startup()

    checks = startup.get_checks()

    assert len(checks) == 5


def test_agents_check_exists():
    """
    Verify agent check.
    """

    startup = Startup()

    checks = startup.get_checks()

    assert (
        "Loading Agents"
        in checks
    )


def test_run_returns_checks():
    """
    Verify execution.
    """

    startup = Startup()

    result = startup.run()

    assert len(result) == 5
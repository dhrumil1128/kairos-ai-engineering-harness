"""
File:
tests/unit/cli/test_main.py

Purpose:
Verify CLI entrypoint.
"""

from main import (
    create_cli
)


def test_cli_creation():
    """
    Verify CLI creation.
    """

    cli = create_cli()

    assert cli is not None


def test_banner_exists():
    """
    Verify banner exists.
    """

    cli = create_cli()

    assert "banner" in cli


def test_startup_exists():
    """
    Verify startup exists.
    """

    cli = create_cli()

    assert "startup" in cli


def test_prompt_exists():
    """
    Verify prompt exists.
    """

    cli = create_cli()

    assert "prompt" in cli
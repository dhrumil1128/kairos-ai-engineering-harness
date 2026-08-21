"""
File:
tests/unit/cli/test_banner.py

Purpose:
Verify banner rendering.
"""

from core.cli.banner import (
    Banner
)


def test_banner_creation():
    """
    Verify creation.
    """

    banner = Banner()

    assert banner is not None


def test_banner_render():
    """
    Verify content.
    """

    banner = Banner()

    output = banner.render()

    assert "KAIROS" in output


def test_banner_contains_tagline():
    """
    Verify tagline.
    """

    banner = Banner()

    output = banner.render()

    assert (
        "Multi-Agent"
        in output
    )


def test_display_exists():
    """
    Verify display method.
    """

    banner = Banner()

    assert hasattr(
        banner,
        "display"
    )
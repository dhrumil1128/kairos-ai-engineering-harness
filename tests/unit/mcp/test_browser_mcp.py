"""
File:
tests/unit/mcp/
test_browser_mcp.py

Purpose:
Verify real Browser MCP.
"""

from core.mcp.browser_mcp import (
    BrowserMCP
)


def test_creation():
    """
    Verify creation.
    """

    mcp = BrowserMCP()

    assert mcp is not None


def test_connection():
    """
    Verify connection.
    """

    mcp = BrowserMCP()

    assert (
        mcp.is_connected()
        is True
    )


def test_get_title():
    """
    Verify title extraction.
    """

    mcp = BrowserMCP()

    title = mcp.get_title(
        "https://example.com"
    )

    assert (
        "Example"
        in title
    )


def test_extract_text():
    """
    Verify text extraction.
    """

    mcp = BrowserMCP()

    text = mcp.extract_text(
        "https://example.com"
    )

    assert (
        len(text) > 0
    )
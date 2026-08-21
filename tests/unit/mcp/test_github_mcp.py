"""
File:
tests/unit/mcp/
test_github_mcp.py

Purpose:
Verify real GitHub MCP.
"""

import os

import pytest

from dotenv import load_dotenv

from core.mcp.github_mcp import (
    GitHubMCP
)


load_dotenv()

TOKEN = os.getenv(
    "GITHUB_TOKEN"
)


@pytest.mark.skipif(
    not TOKEN,
    reason="GITHUB_TOKEN not configured"
)
def test_connection():
    """
    Verify GitHub connection.
    """

    mcp = GitHubMCP()

    assert (
        mcp.is_connected()
        is True
    )


@pytest.mark.skipif(
    not TOKEN,
    reason="GITHUB_TOKEN not configured"
)
def test_repository_lookup():
    """
    Verify repository lookup.
    """

    mcp = GitHubMCP()

    repo = mcp.get_repository(
        "microsoft/vscode"
    )

    assert (
        repo["name"]
        == "microsoft/vscode"
    )


@pytest.mark.skipif(
    not TOKEN,
    reason="GITHUB_TOKEN not configured"
)
def test_repository_has_branch():
    """
    Verify default branch.
    """

    mcp = GitHubMCP()

    repo = mcp.get_repository(
        "microsoft/vscode"
    )

    assert (
        len(
            repo["default_branch"]
        )
        > 0
    )


@pytest.mark.skipif(
    not TOKEN,
    reason="GITHUB_TOKEN not configured"
)
def test_repository_has_language():
    """
    Verify language metadata.
    """

    mcp = GitHubMCP()

    repo = mcp.get_repository(
        "microsoft/vscode"
    )

    assert (
        repo["language"]
        is not None
    )
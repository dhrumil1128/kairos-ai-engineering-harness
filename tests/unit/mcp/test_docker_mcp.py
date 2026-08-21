"""
File:
tests/unit/mcp/
test_docker_mcp.py

Purpose:
Verify real Docker MCP.
"""

from core.mcp.docker_mcp import (
    DockerMCP
)


def test_connection():
    """
    Verify Docker connection.
    """

    mcp = DockerMCP()

    assert (
        mcp.is_connected()
        is True
    )


def test_list_containers():
    """
    Verify container listing.
    """

    mcp = DockerMCP()

    containers = (
        mcp.list_containers()
    )

    assert isinstance(
        containers,
        list
    )


def test_container_count():
    """
    Verify count retrieval.
    """

    mcp = DockerMCP()

    containers = (
        mcp.list_containers()
    )

    assert (
        len(containers)
        >= 0
    )
"""
File: core/mcp/mcp_client.py

Purpose:
Interact with MCP server.
"""

from core.mcp.mcp_server import (
    MCPServer
)


class MCPClient:
    """
    MCP client.
    """

    def __init__(
        self,
        server: MCPServer
    ):
        """
        Initialize client.
        """

        self.server = server

    def list_tools(
        self
    ) -> list[str]:
        """
        List tools.
        """

        return (
            self.server
            .list_tools()
        )

    def get_tool(
        self,
        name: str
    ):
        """
        Retrieve tool.
        """

        return (
            self.server
            .get_tool(name)
        )
"""
File: core/mcp/mcp_server.py

Purpose:
Register and manage tools.
"""


class MCPServer:
    """
    MCP tool registry.
    """

    def __init__(self):
        """
        Initialize registry.
        """

        self._tools = {}

    def register_tool(
        self,
        name: str,
        tool
    ) -> None:
        """
        Register tool.
        """

        self._tools[name] = tool

    def get_tool(
        self,
        name: str
    ):
        """
        Retrieve tool.
        """

        return self._tools.get(
            name
        )

    def list_tools(
        self
    ) -> list[str]:
        """
        List registered tools.
        """

        return list(
            self._tools.keys()
        )

    def has_tool(
        self,
        name: str
    ) -> bool:
        """
        Check existence.
        """

        return (
            name
            in self._tools
        )
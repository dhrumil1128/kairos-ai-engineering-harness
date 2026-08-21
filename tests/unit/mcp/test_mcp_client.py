from core.mcp.mcp_client import (
    MCPClient
)

from core.mcp.mcp_server import (
    MCPServer
)


def test_client_creation():

    server = MCPServer()

    client = MCPClient(
        server
    )

    assert client is not None


def test_client_list_tools():

    server = MCPServer()

    server.register_tool(
        "tool_a",
        object()
    )

    client = MCPClient(
        server
    )

    assert (
        "tool_a"
        in client.list_tools()
    )


def test_client_get_tool():

    server = MCPServer()

    tool = object()

    server.register_tool(
        "tool_a",
        tool
    )

    client = MCPClient(
        server
    )

    assert (
        client.get_tool(
            "tool_a"
        )
        is tool
    )
from core.mcp.mcp_server import (
    MCPServer
)


def test_register_tool():

    server = MCPServer()

    server.register_tool(
        "tool_a",
        object()
    )

    assert (
        server.has_tool(
            "tool_a"
        )
        is True
    )


def test_get_tool():

    server = MCPServer()

    tool = object()

    server.register_tool(
        "tool_a",
        tool
    )

    assert (
        server.get_tool(
            "tool_a"
        )
        is tool
    )


def test_list_tools():

    server = MCPServer()

    server.register_tool(
        "a",
        object()
    )

    server.register_tool(
        "b",
        object()
    )

    assert (
        len(
            server.list_tools()
        )
        == 2
    )
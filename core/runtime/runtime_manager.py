"""
File: core/runtime/runtime_manager.py

Purpose:
Initialize and manage
KAIROS runtime services.

Responsibilities:

- Register MCPs
- Register Plugins
- Provide access
"""

from core.mcp.mcp_server import (
    MCPServer
)

from core.plugins.plugin_manager import (
    PluginManager
)

from core.mcp.browser_mcp import (
    BrowserMCP
)

from core.mcp.database_mcp import (
    DatabaseMCP
)

from core.mcp.docker_mcp import (
    DockerMCP
)

from core.mcp.github_mcp import (
    GitHubMCP
)

from core.plugins.browser_plugin import (
    BrowserPlugin
)

from core.plugins.documentation_plugin import (
    DocumentationPlugin
)

from core.plugins.filesystem_plugin import (
    FilesystemPlugin
)

from core.plugins.git_plugin import (
    GitPlugin
)

from core.plugins.security_plugin import (
    SecurityPlugin
)

from core.plugins.terminal_plugin import (
    TerminalPlugin
)

from core.plugins.testing_plugin import (
    TestingPlugin
)


class RuntimeManager:
    """
    KAIROS runtime manager.
    """

    def __init__(self):
        """
        Initialize runtime.
        """

        self.mcp_server = MCPServer()

        self.plugin_manager = (
            PluginManager()
        )
        
        self.active_project = r"E:\KAIROS"

    def register_mcps(self):
        """
        Register MCP tools.
        """

        self.mcp_server.register_tool(
            "BrowserMCP",
            BrowserMCP()
        )

        self.mcp_server.register_tool(
            "DatabaseMCP",
            DatabaseMCP()
        )

        # Docker/GitHub may fail
        # if environment not ready.

        try:

            self.mcp_server.register_tool(
                "DockerMCP",
                DockerMCP()
            )

        except Exception:
            pass

        try:

            self.mcp_server.register_tool(
                "GitHubMCP",
                GitHubMCP()
            )

        except Exception:
            pass

    def register_plugins(self):
        """
        Register plugins.
        """

        self.plugin_manager.register_plugin(
            "BrowserPlugin",
            BrowserPlugin()
        )

        self.plugin_manager.register_plugin(
            "DocumentationPlugin",
            DocumentationPlugin(self)
        )

        self.plugin_manager.register_plugin(
            "FilesystemPlugin",
            FilesystemPlugin()
        )

        self.plugin_manager.register_plugin(
            "GitPlugin",
            GitPlugin()
        )

        self.plugin_manager.register_plugin(
            "SecurityPlugin",
            SecurityPlugin()
        )

        self.plugin_manager.register_plugin(
            "TerminalPlugin",
            TerminalPlugin()
        )

        self.plugin_manager.register_plugin(
            "TestingPlugin",
            TestingPlugin()
        )


    # add the active project directory 
    def set_active_project(
    self,
    path: str
    ):

        self.active_project = path


    def get_active_project(
        self
    ):

        return self.active_project
    
    
    def initialize(self):
        """
        Initialize runtime.
        """

        self.register_mcps()

        self.register_plugins()
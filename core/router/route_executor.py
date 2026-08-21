"""
File: core/router/route_executor.py

Purpose:
Execute structured intents
through the correct
Agent, Plugin, or MCP.

Why:

TaskRouter identifies
the category.

IntentHandler extracts
the action.

RouteExecutor performs
the actual execution.

Architecture:

User Prompt
      ↓
TaskRouter
      ↓
IntentHandler
      ↓
RouteExecutor
      ↓
Plugin / MCP / Agent
      ↓
Result

V1:
- Single action execution
- Plugin execution
- MCP execution

V2:
- Multi-step execution

V3:
- Chained tool execution

V4:
- Agent collaboration

V5:
- Autonomous workflows

Enterprise:

- Workflow engine
- Tool orchestration
- Multi-agent execution
- Approval pipelines
- Governance controls
"""
import time

class RouteExecutor:
    """
    Execute parsed intents.
    """

    def __init__(
        self,
        filesystem,
        desktop,
        runtime
    ):
        """
        Initialize executor.
        """

        # Filesystem plugin.
        self.filesystem = (
            filesystem
        )

        # Desktop controller.
        self.desktop = (
            desktop
        )

        # Runtime manager.
        self.runtime = (
            runtime
        )

    def execute(
        self,
        intent: dict
    ) -> dict:
        """
        Execute intent.
        """

        
        action = (
            intent.get(
                "action"
            )
        )

        target = (
            intent.get(
                "target"
            )
        )
        
        value = (
            intent.get(
                "value"
            )
        )

       
        
        
        # waiting time 
        if action == "wait_seconds":

            time.sleep(
                int(target)
            )

            return {
                "status": "success",
                "message":
                    f"Waited {target} seconds"
            }

        # ==================================================
        # FILESYSTEM PLUGIN
        # ==================================================

        if action == "create_directory":

            self.filesystem.execute(
                "create_directory",
                target
            )

            return {
                "status": "success",
                "message":
                    f"Directory created: workspace/{target}"
            }

        if action == "delete_directory":

            self.filesystem.execute(
                "delete",
                f"workspace/{target}"
            )

            return {
                "status": "success",
                "message":
                    f"Directory deleted: workspace/{target}"
            }

        if action == "create_file":

            self.filesystem.execute(
                "write",
                target,
                value
            )

            return {
                "status": "success",
                "message":
                    f"File created: workspace/{target}"
            }

        if action == "list_directory":

            result = (
                self.filesystem.execute(
                    "list_directory",
                    target
                )
            )

            return {
                "status": "success",
                "message": result
            }

        if action == "file_exists":

            result = (
                self.filesystem.execute(
                    "exists",
                    target
                )
            )

            return {
                "status": "success",
                "message": result
            }

        if action == "init_project":

            self.filesystem.execute(
                "init_project",
                target
            )

            return {
                "status": "success",
                "message":
                    f"KAIROS project initialized: {target}"
            }

        
        # ==================================================
        # BROWSER PLUGIN
        # ==================================================

        if action == "open_url":

            plugin = (
                self.runtime
                .plugin_manager
                .get_plugin(
                    "BrowserPlugin"
                )
            )

            result = (
                plugin.execute(
                    target
                )
            )

            return {
                "status": "success",
                "message": result
            }

        # ==================================================
        # DOCUMENTATION PLUGIN
        # ==================================================

        if action == "generate_documentation":

            plugin = (
                self.runtime
                .plugin_manager
                .get_plugin(
                    "DocumentationPlugin"
                )
            )

            result = (
                plugin.execute(
                    target
                )
            )

            return {
                "status": "success",
                "message": result
            }

        # ==================================================
        # GIT PLUGIN
        # ==================================================

        if action == "git_status":

            plugin = (
                self.runtime
                .plugin_manager
                .get_plugin(
                    "GitPlugin"
                )
            )

            result = (
                plugin.execute(
                    "status"
                )
            )

            return {
                "status": "success",
                "message": result
            }

        if action == "git_branch":

            plugin = (
                self.runtime
                .plugin_manager
                .get_plugin(
                    "GitPlugin"
                )
            )

            result = (
                plugin.execute(
                    "branch"
                )
            )

            return {
                "status": "success",
                "message": result
            }

        # ==================================================
        # SECURITY PLUGIN
        # ==================================================

        if action == "security_scan":

            plugin = (
                self.runtime
                .plugin_manager
                .get_plugin(
                    "SecurityPlugin"
                )
            )

            result = (
                plugin.execute(
                    target
                )
            )

            return {
                "status": "success",
                "message": result
            }

        # ==================================================
        # TERMINAL PLUGIN
        # ==================================================

        if action == "terminal_command":

            plugin = (
                self.runtime
                .plugin_manager
                .get_plugin(
                    "TerminalPlugin"
                )
            )

            result = (
                plugin.execute(
                    target
                )
            )

            return {
                "status": "success",
                "message": result
            }

        # ==================================================
        # TESTING PLUGIN
        # ==================================================

        if action == "analyze_test_output":

            plugin = (
                self.runtime
                .plugin_manager
                .get_plugin(
                    "TestingPlugin"
                )
            )

            result = (
                plugin.execute(
                    target
                )
            )

            return {
                "status": "success",
                "message": result
            }

        # ==================================================
        # DOCKER MCP
        # ==================================================

        if action == "docker_status":

            docker_mcp = (
                self.runtime
                .mcp_server
                .get_tool(
                    "DockerMCP"
                )
            )

            result = (
                docker_mcp.is_connected()
            )

            return {
                "status": "success",
                "message": result
            }

        if action == "docker_containers":

            docker_mcp = (
                self.runtime
                .mcp_server
                .get_tool(
                    "DockerMCP"
                )
            )

            result = (
                docker_mcp.list_containers()
            )

            return {
                "status": "success",
                "message": result
            }

        if action == "docker_container_info":

            docker_mcp = (
                self.runtime
                .mcp_server
                .get_tool(
                    "DockerMCP"
                )
            )

            result = (
                docker_mcp.get_container_info(
                    target
                )
            )

            return {
                "status": "success",
                "message": result
            }

        # ==================================================
        # GITHUB MCP
        # ==================================================

        if action == "github_status":

            github_mcp = (
                self.runtime
                .mcp_server
                .get_tool(
                    "GitHubMCP"
                )
            )

            result = (
                github_mcp.is_connected()
            )

            return {
                "status": "success",
                "message": result
            }

        if action == "github_repository":

            github_mcp = (
                self.runtime
                .mcp_server
                .get_tool(
                    "GitHubMCP"
                )
            )

            result = (
                github_mcp.get_repository(
                    target
                )
            )

            return {
                "status": "success",
                "message": result
            }

        # ==================================================
        # DATABASE MCP
        # ==================================================

        if action == "database_status":

            database_mcp = (
                self.runtime
                .mcp_server
                .get_tool(
                    "DatabaseMCP"
                )
            )

            result = (
                database_mcp.is_connected()
            )

            return {
                "status": "success",
                "message": result
            }

        if action == "database_execute_query":

            database_mcp = (
                self.runtime
                .mcp_server
                .get_tool(
                    "DatabaseMCP"
                )
            )

            result = (
                database_mcp.execute_query(
                    target
                )
            )

            return {
                "status": "success",
                "message": result
            }

        if action == "database_fetch_one":

            database_mcp = (
                self.runtime
                .mcp_server
                .get_tool(
                    "DatabaseMCP"
                )
            )

            result = (
                database_mcp.fetch_one(
                    target
                )
            )

            return {
                "status": "success",
                "message": result
            }

        # ==================================================
        # BROWSER MCP
        # ==================================================

        if action == "browser_status":

            browser_mcp = (
                self.runtime
                .mcp_server
                .get_tool(
                    "BrowserMCP"
                )
            )

            result = (
                browser_mcp.is_connected()
            )

            return {
                "status": "success",
                "message": result
            }

        if action == "browser_title":

            browser_mcp = (
                self.runtime
                .mcp_server
                .get_tool(
                    "BrowserMCP"
                )
            )

            result = (
                browser_mcp.get_title(
                    target
                )
            )

            return {
                "status": "success",
                "message": result
            }

        if action == "browser_extract_text":

            browser_mcp = (
                self.runtime
                .mcp_server
                .get_tool(
                    "BrowserMCP"
                )
            )

            result = (
                browser_mcp.extract_text(
                    target
                )
            )

            return {
                "status": "success",
                "message": result
            }
            

        # ==================================================
        # DESKTOP WORKFLOW
        # ==================================================
        desktop_actions = {

            "open_application":
                lambda: self.desktop.launch_application(
                    target,
                    value
                ),
            "open_browser":
                lambda: self.desktop.open_browser(
                
                        target
                      
                    
                ),

            "navigate_url":
                lambda: self.desktop.navigate_url(
                  
                        target
                     
                    
                ),

            "browser_search":
                lambda: self.desktop.browser_search(
                   
                        target,
                        
                    
                ),

            "new_tab":
                lambda: self.desktop.new_tab(),

            "close_tab":
                lambda: self.desktop.close_tab(),

            "refresh_browser":
                lambda: self.desktop.refresh_browser(),

            "browser_back":
                lambda: self.desktop.browser_back(),

            "browser_forward":
                lambda: self.desktop.browser_forward(),

            "browser_history":
                lambda: self.desktop.browser_history(),

            "browser_downloads":
                lambda: self.desktop.browser_downloads(),

            "close_browser":
                lambda: self.desktop.close_browser(),
    
    
            "focus_window":
                lambda: self.desktop.focus_window(
                    target
                ),

            "type_text":
                lambda: self.desktop.type_text(
                    value
                ),

            "press_key":
                lambda: self.desktop.press_key(
                    value
                ),

            "mouse_click":
                lambda: self.desktop.click(target),

            "double_click":
                lambda: self.desktop.double_click(),

            "move_mouse":
                lambda: self.desktop.move_mouse(
                    target[0],
                    target[1]
                ),

            "window_titles":
                lambda: self.desktop.get_windows(),

            "list_processes":
                lambda: self.desktop.list_processes(),

            "mouse_position":
                lambda: self.desktop.get_mouse_position(),
        }

        if action in desktop_actions:

            result = desktop_actions[action]()

            return {
                "status": "success",
                "message": result,
            }
        
        return {
            "status": "failed",
            "message": f"Unsupported action: {action}",
        }
                
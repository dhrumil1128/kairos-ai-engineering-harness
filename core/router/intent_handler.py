"""
File: core/router/intent_handler.py

Purpose:
Convert natural language
commands into structured
actions.

Why:

TaskRouter determines
the category.

IntentHandler determines
the exact action.

Architecture:

User Prompt
      ↓
TaskRouter
      ↓
IntentHandler
      ↓
Structured Intent
      ↓
RouteExecutor
      ↓
Plugin / MCP / Agent

V1:
- Rule-based intent extraction
- Plugin routing
- MCP routing

V2:
- Regex extraction

V3:
- Entity extraction

V4:
- LLM intent parsing

V5:
- Multi-step actions

Enterprise:

- Workflow extraction
- Agent orchestration
- Multi-tool execution
- Context-aware actions
"""


class IntentHandler:
    """
    Extract actionable intents
    from user commands.
    """

    def parse(
        self,
        command: str,
        task_type: str
    ) -> dict:
        """
        Parse user command.
        """

        command_lower = (
            command.lower()
        )

        # ==================================================
        # FILESYSTEM PLUGIN
        # ==================================================

        if task_type == "filesystem":

            if (
                command_lower.startswith(
                    "create folder "
                )
            ):

                target = (
                    command.replace(
                        "Create folder ",
                        ""
                    ).strip()
                )

                return {
                    "action":
                        "create_directory",
                    "target":
                        target
                }

            if (
                command_lower.startswith(
                    "delete folder "
                )
            ):

                target = (
                    command.replace(
                        "Delete folder ",
                        ""
                    ).strip()
                )

                return {
                    "action":
                        "delete_directory",
                    "target":
                        target
                }

            if (
                command_lower.startswith(
                    "create file "
                )
            ):

                target = (
                    command.replace(
                        "Create file ",
                        ""
                    ).strip()
                )

                return {
                    "action":
                        "create_file",
                    "target":
                        target
                }

            if (
                command_lower.startswith(
                    "list directory "
                )
            ):

                target = (
                    command.replace(
                        "List directory ",
                        ""
                    ).strip()
                )

                return {
                    "action":
                        "list_directory",
                    "target":
                        target
                }

            if (
                command_lower.startswith(
                    "check file "
                )
            ):

                target = (
                    command.replace(
                        "Check file ",
                        ""
                    ).strip()
                )

                return {
                    "action":
                        "file_exists",
                    "target":
                        target
                }

            if (
                command_lower.startswith(
                    "initialize project "
                )
            ):

                target = (
                    command.replace(
                        "Initialize project ",
                        ""
                    ).strip()
                )

                return {
                    "action":
                        "init_project",
                    "target":
                        target
                }

        # ==================================================
        # DESKTOP AGENT
        # ==================================================

        if task_type == "desktop":

            if (
                "open notepad"
                in command_lower
            ):

                return {
                    "action":
                        "open_application",
                    "target":
                        "notepad"
                }

            if (
                "open calculator"
                in command_lower
            ):

                return {
                    "action":
                        "open_application",
                    "target":
                        "calculator"
                }

        # ==================================================
        # BROWSER PLUGIN
        # ==================================================

        if (
            command_lower.startswith(
                "open website "
            )
        ):

            target = (
                command.replace(
                    "Open website ",
                    ""
                ).strip()
            )

            return {
                "action":
                    "open_url",
                "target":
                    target
            }

        # ==================================================
        # DOCUMENTATION PLUGIN
        # ==================================================

        if (
            command_lower.startswith(
                "generate documentation for "
            )
        ):

            target = (
                command.replace(
                    "Generate documentation for ",
                    ""
                ).strip()
            )

            return {
                "action":
                    "generate_documentation",
                "target":
                    target
            }

        # ==================================================
        # GIT PLUGIN
        # ==================================================

        if (
            "git status"
            in command_lower
        ):

            return {
                "action":
                    "git_status",
                "target":
                    None
            }

        if (
            "git branch"
            in command_lower
        ):

            return {
                "action":
                    "git_branch",
                "target":
                    None
            }

        # ==================================================
        # SECURITY PLUGIN
        # ==================================================

        if (
            command_lower.startswith(
                "check security "
            )
        ):

            target = (
                command.replace(
                    "Check security ",
                    ""
                ).strip()
            )

            return {
                "action":
                    "security_scan",
                "target":
                    target
            }

        # ==================================================
        # TERMINAL PLUGIN
        # ==================================================

        if (
            command_lower.startswith(
                "run terminal command "
            )
        ):

            target = (
                command.replace(
                    "Run terminal command ",
                    ""
                ).strip()
            )

            return {
                "action":
                    "terminal_command",
                "target":
                    target
            }

        # ==================================================
        # TESTING PLUGIN
        # ==================================================

        if (
            command_lower.startswith(
                "analyze test output "
            )
        ):

            target = (
                command.replace(
                    "Analyze test output ",
                    ""
                ).strip()
            )

            return {
                "action":
                    "analyze_test_output",
                "target":
                    target
            }

        # ==================================================
        # DOCKER MCP
        # ==================================================

        if (
            "docker status"
            in command_lower
        ):

            return {
                "action":
                    "docker_status",
                "target":
                    None
            }

        if (
            "docker containers"
            in command_lower
        ):

            return {
                "action":
                    "docker_containers",
                "target":
                    None
            }

        if (
            "docker container"
            in command_lower
        ):

            target = (
                command_lower
                .replace(
                    "show docker container",
                    ""
                )
                .replace(
                    "docker container",
                    ""
                )
                .strip()
            )

            return {
                "action":
                    "docker_container_info",
                "target":
                    target
            }

        # ==================================================
        # GITHUB MCP
        # ==================================================

        if (
            "github status"
            in command_lower
        ):

            return {
                "action":
                    "github_status",
                "target":
                    None
            }

        if (
            "github repository"
            in command_lower
        ):

            target = (
                command_lower
                .replace(
                    "show github repository",
                    ""
                )
                .replace(
                    "github repository",
                    ""
                )
                .strip()
            )

            return {
                "action":
                    "github_repository",
                "target":
                    target
            }

        # ==================================================
        # DATABASE MCP
        # ==================================================

        if (
            "database status"
            in command_lower
        ):

            return {
                "action":
                    "database_status",
                "target":
                    None
            }

        if (
            command_lower.startswith(
                "execute query "
            )
        ):

            target = (
                command.replace(
                    "Execute query ",
                    ""
                ).strip()
            )

            return {
                "action":
                    "database_execute_query",
                "target":
                    target
            }

        if (
            command_lower.startswith(
                "fetch one "
            )
        ):

            target = (
                command.replace(
                    "Fetch one ",
                    ""
                ).strip()
            )

            return {
                "action":
                    "database_fetch_one",
                "target":
                    target
            }

        # ==================================================
        # BROWSER MCP
        # ==================================================

        if (
            "browser status"
            in command_lower
        ):

            return {
                "action":
                    "browser_status",
                "target":
                    None
            }

        if (
            command_lower.startswith(
                "get title "
            )
        ):

            target = (
                command.replace(
                    "Get title ",
                    ""
                ).strip()
            )

            return {
                "action":
                    "browser_title",
                "target":
                    target
            }

        if (
            command_lower.startswith(
                "extract text "
            )
        ):

            target = (
                command.replace(
                    "Extract text ",
                    ""
                ).strip()
            )

            return {
                "action":
                    "browser_extract_text",
                "target":
                    target
            }




        
        # ==================================================
        # DESKTOP WORKFLOW
        # ==================================================

        if task_type == "desktop":

            if (
                command_lower.startswith(
                    "type "
                )
            ):

                target = (
                    command.replace(
                        "Type ",
                        ""
                    ).strip()
                )

                return {
                    "action":
                        "type_text",

                    "target":
                        target
                }

            if (
                command_lower.startswith(
                    "press "
                )
            ):

                target = (
                    command.replace(
                        "Press ",
                        ""
                    ).strip()
                )

                return {
                    "action":
                        "press_key",

                    "target":
                        target
                }

            if (
                command_lower.startswith(
                    "focus "
                )
            ):

                target = (
                    command.replace(
                        "Focus ",
                        ""
                    ).strip()
                )

                return {
                    "action":
                        "focus_window",

                    "target":
                        target
                }

            if (
                command_lower == "click mouse"
            ):

                return {
                    "action":
                        "mouse_click",

                    "target":
                        None
                }

            if (
                command_lower.startswith(
                    "move mouse "
                )
            ):

                target = (
                    command.replace(
                        "Move mouse ",
                        ""
                    ).strip()
                )

                return {
                    "action":
                        "move_mouse",

                    "target":
                        target
                }
        # ==================================================
        # DEFAULT
        # ==================================================

        return {
            "action":
                "software_pipeline",
            "target":
                command
        }

    def is_supported(
        self,
        intent: dict
    ) -> bool:

        return (
            intent.get(
                "action"
            )
            != "software_pipeline"
        )

    def get_action(
        self,
        intent: dict
    ) -> str:

        return intent.get(
            "action"
        )

    def get_target(
        self,
        intent: dict
    ):

        return intent.get(
            "target"
        )
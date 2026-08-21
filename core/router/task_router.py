"""
File: core/router/task_router.py

Purpose:
Route user tasks to the
correct subsystem.

Why:

Not every prompt should
go through the software
generation pipeline.

Some prompts should be
handled by plugins,
desktop agents, browsers,
or MCPs.

Architecture:

User Prompt
      ↓
TaskRouter
      ↓
Desktop Agent
Browser Agent
Filesystem Plugin
Software Pipeline

V1:
- Keyword routing

V2:
- Intent classification

V3:
- LLM routing

V4:
- Multi-agent routing

V5:
- Autonomous orchestration

Enterprise:

- Policy routing
- Cost-aware routing
- Multi-model routing
- Team workflows
"""


class TaskRouter:
    """
    Route tasks to
    subsystems.
    """

    def route(
        self,
        command: str
    ) -> str:
        """
        Route command.

        Returns:

        desktop
        browser
        filesystem
        software
        """

        command = (
            command.lower()
        )

        # ------------------
        # Desktop Tasks
        # ------------------

        desktop_keywords = [

    "open",
    "close",

    "type",
    "press",

    "focus",

    "click",
    "double click",

    "move mouse",

    "scroll",

    "desktop",

    "window",

    "keyboard",

    "mouse"
]

        if any(
            keyword in command
            for keyword in desktop_keywords
        ):

            return "desktop"

        # ------------------
        # Browser Tasks
        # ------------------

        browser_keywords = [

    "browser",

    "chrome",
    "edge",
    "firefox",

    "google",

    "youtube",

    "search",

    "website",

    "navigate",

    "visit"
]

        if any(
            keyword in command
            for keyword in browser_keywords
        ):

            return "browser"

        # ------------------
        # Filesystem Tasks
        # ------------------

        filesystem_keywords = [

    "file",

    "folder",

    "directory",

    "create folder",

    "create directory",

    "create file",

    "read file",

    "write file",

    "delete file",

    "delete folder",

    "list files",

    "list directory",

    "rename",

    "copy",

    "move"
]

        if any(
            keyword in command
            for keyword in filesystem_keywords
        ):

            return "filesystem"

        # ------------------
        # Default
        # ------------------

        return "software" 
"""
File: core/router/workflow_planner.py
This file is mainly for the Desktop Automation . 

Purpose:
Convert natural language
requests into executable
workflow plans.

Why:

IntentHandler handles
single actions.

WorkflowPlanner handles
multi-step workflows.

Instead of hardcoding:

- YouTube
- Google
- Chrome
- Firefox
- Instagram

we allow the currently
selected LLM to generate
the workflow dynamically.

Architecture:

User Prompt
      ↓
WorkflowPlanner
      ↓
ProviderManager
      ↓
Current Session Model
      ↓
JSON Workflow
      ↓
Validation
      ↓
RouteExecutor

V1:
- LLM workflow planning

V2:
- Workflow validation

V3:
- Workflow optimization

V4:
- Workflow memory

V5:
- Autonomous planning

Enterprise:

- Multi-agent planning
- Workflow caching
- Policy-aware planning
- Cost-aware planning
"""

import json

from core.providers.provider_manager import (
    ProviderManager
)

from core.providers.provider_registry import (
    ProviderRegistry
)


class WorkflowPlanner:
    """
    Dynamic workflow planner.
    """

    def __init__(
        self
    ):
        """
        Initialize planner.
        """

        self.provider_manager = (
            ProviderManager(
                ProviderRegistry()
            )
        )

        self.provider = (
            "ollama"
        )

    def create_workflow(
        self,
        command: str
    ) -> list[dict]:
        """
        Create workflow
        from natural language.
        """

        prompt = f"""
You are KAIROS Desktop Workflow Planner.

Your sole responsibility is to convert the user's request into a deterministic desktop automation workflow.

You DO NOT execute actions.
You DO NOT generate Python code.
You DO NOT explain your reasoning.
You ONLY produce a valid JSON workflow.

==================================================
INTERNAL IMPLEMENTATION DETAILS - NEVER OUTPUT
==================================================

The following names are internal implementation details only.
They are never valid workflow actions.
They are never valid workflow targets.
They must never appear anywhere in the generated JSON.

Never generate these names:

- ApplicationController
- BrowserController
- DesktopController
- WindowController
- KeyboardController
- MouseController
- ClipboardController
- FileController
- BrowserPlugin
- DesktopPlugin
- FilesystemPlugin
- ShellPlugin
- Browser MCP
- Desktop MCP
- Filesystem MCP
- Terminal MCP

Do not open an implementation detail.
Do not focus an implementation detail.
Do not use an implementation detail as a target.
Do not generate Python class names, plugin names, MCP names, or controller names.

==================================================
RULES
==================================================

1. Understand the user's final objective.
2. Produce the minimum number of actions.
3. Preserve execution order.
4. Every action must be executable.
5. Reuse existing applications whenever possible.
6. Reuse existing browser windows whenever possible.
7. Wait only when required.
8. Never invent unsupported actions.
9. Never skip required steps.
10. Continue until the objective is complete.
11. Never generate Python code.
12. Never return markdown.
13. Never return explanations.
14. Never return text outside the JSON.
15. Return valid JSON only.
16. Never generate redundant actions.
17. Prefer direct URL navigation whenever possible.
18. Generate the minimum executable workflow that satisfies the task.
19. Generate only supported workflow actions.
20. Never generate controller names, plugin names, MCP names, or Python class names.
21. Internal implementation details are never valid workflow targets.
22. For filesystem requests, operate directly on the requested path.
23. Do not open File Explorer for filesystem actions.
25. If the user does not specify an absolute path, treat the path as relative to the current workspace.
Do not invent drive letters such as C:\ or D:\.
Only use an absolute path if the user explicitly provides one.

==================================================
TERMINAL ACTIONS
==================================================

A terminal action is an action that fully satisfies the user's intent.

When a terminal action completes the objective, stop the workflow immediately.
Do not add UI actions after it.

Browser terminal actions:

- open_browser is terminal for requests that only ask to open a browser.
- navigate_url is terminal when its URL already represents the final page,
  destination, search results, video, document, repository, or website requested
  by the user.
- open_url is terminal when its URL already represents the final destination.

If navigate_url already completes the user's objective, DO NOT generate any of
these follow-up actions:

- type_text
- press_key
- mouse_click
- browser_search

Examples of terminal navigation:

- YouTube search:
  navigate_url("https://www.youtube.com/results?search_query=OpenAI")
  This already completes "search OpenAI on YouTube".

- Google search:
  navigate_url("https://www.google.com/search?q=OpenAI")
  This already completes "search OpenAI on Google".

- GitHub repository:
  navigate_url("https://github.com/openai/openai-python")
  This already completes "open the OpenAI Python repo".

Only use type_text, press_key, mouse_click, or browser_search when direct URL
navigation cannot complete the user's objective.

Never type a URL into the address bar manually.
Never press Enter after a navigate_url action.
Never search again after navigating directly to a search results URL.
Never click generic targets like "first_result" or "first_video" unless the user
explicitly asks to open or play a result and no deterministic direct URL exists.

==================================================
SUPPORTED ACTIONS
==================================================

Applications
- open_application

Browser
- open_browser
- open_url
- navigate_url
- browser_search
- new_tab
- close_tab
- refresh_browser
- browser_back
- browser_forward
- browser_history
- browser_downloads
- close_browser

Window
- focus_window

Keyboard
- type_text
- press_key

Mouse
- move_mouse
- mouse_click
- double_click

Filesystem
- create_directory
- delete_directory
- create_file

Desktop
- wait_seconds

Terminal
- terminal_command

Git
- git_status
- git_branch

Browser Extraction
- browser_title
- browser_extract_text

Security
- security_scan

Database
- database_execute_query

==================================================
WORKFLOW FORMAT
==================================================

Return exactly this structure.

{{
    "workflow": [
        {{
            "id": 1,
            "action": "",
            "target": "",
            "value": "",
            "parameters": {{}},
            "wait_after": 0
        }}
    ]
}}

================================================
Keyboard Examples
===================================

User:
Open Notepad and press Ctrl+S.

Output

{{
    
  "workflow": [
    {{
      "id": 1,
      "action": "open_application",
      "target": "notepad",
      "value": "",
      "parameters": {{}},
      "wait_after": 1
    }},
    
    {{
      "id": 2,
      "action": "press_key",
      "target": "notepad",
      "value": "ctrl+s",
      "parameters": {{}},
      "wait_after": 0
    }}
  ]
}}

User:
Close Notepad.

Output

{{
  "workflow": [
    {{
      "id": 1,
      "action": "press_key",
      "target": "notepad",
      "value": "alt+f4",
      "parameters": {{}},
      "wait_after": 0
    }}
  ]
}}



==================================================
FIELD DEFINITIONS
==================================================

id
    Sequential integer starting from 1.

action
    One supported action.

target
    The object the action operates on.

value
    Optional input value.

parameters
    Additional structured parameters.
    Use {{}} when unused.

wait_after
    Seconds to wait after executing the action.
    Use 0 when unnecessary.

For websites that support URL-based search, such as YouTube, Google, GitHub,
Stack Overflow, documentation sites, or package registries, generate a final
destination URL with navigate_url instead of using keyboard or mouse actions.

==================================================
MINIMAL BROWSER EXAMPLES
==================================================

User:

Open Chrome.

Output

{{
    "workflow": [
        {{
            "id": 1,
            "action": "open_browser",
            "target": "chrome",
            "value": "",
            "parameters": {{}},
            "wait_after": 0
        }}
    ]
}}

User:

Open Chrome and go to YouTube.

Output

{{
    "workflow": [
        {{
            "id": 1,
            "action": "open_browser",
            "target": "chrome",
            "value": "",
            "parameters": {{}},
            "wait_after": 1
        }},
        {{
            "id": 2,
            "action": "navigate_url",
            "target": "https://www.youtube.com",
            "value": "",
            "parameters": {{}},
            "wait_after": 0
        }}
    ]
}}

User:

Open Chrome and search OpenAI on YouTube.

Output

{{
    "workflow": [
        {{
            "id": 1,
            "action": "open_browser",
            "target": "chrome",
            "value": "",
            "parameters": {{}},
            "wait_after": 1
        }},
        {{
            "id": 2,
            "action": "navigate_url",
            "target": "https://www.youtube.com/results?search_query=OpenAI",
            "value": "",
            "parameters": {{}},
            "wait_after": 0
        }}
    ]
}}

User:

Open Chrome and search OpenAI on Google.

Output

{{
    "workflow": [
        {{
            "id": 1,
            "action": "open_browser",
            "target": "chrome",
            "value": "",
            "parameters": {{}},
            "wait_after": 1
        }},
        {{
            "id": 2,
            "action": "navigate_url",
            "target": "https://www.google.com/search?q=OpenAI",
            "value": "",
            "parameters": {{}},
            "wait_after": 0
        }}
    ]
}}

==================================================
MINIMAL FILESYSTEM EXAMPLES
==================================================

User:

Create a folder named Jarvis in D:\\

Output

{{
    "workflow": [
        {{
            "id": 1,
            "action": "create_directory",
            "target": "D:\\\\Jarvis",
            "value": "",
            "parameters": {{}},
            "wait_after": 0
        }}
    ]
}}

User:

Create a folder named Logs.

Output

{{
    "workflow": [
        {{
            "id": 1,
            "action": "create_directory",
            "target": "Logs",
            "value": "",
            "parameters": {{}},
            "wait_after": 0
        }}
    ]
}}

For filesystem-only requests:

- Do not open File Explorer.
- Do not open any application.
- Do not generate open_application.
- Do not generate FileController.
- Generate the minimum executable workflow.
- Put the final filesystem path in target.
- Leave value as "" unless the action specifically needs content.

==================================================
VALIDATION
==================================================

Before returning the response verify:

- Output is valid JSON.
- Output contains only JSON.
- No markdown.
- No comments.
- No explanations.
- "workflow" exists.
- "workflow" is an array.
- Every action has:
  - id
  - action
  - target
  - value
  - parameters
  - wait_after
- IDs are sequential.
- Actions preserve execution order.
- The workflow contains no redundant action.
- The workflow stops after a terminal action completes the user's objective.
- If navigate_url opens the final destination, remove every later type_text,
  press_key, mouse_click, and browser_search action.
- If a direct search URL can satisfy the task, use navigate_url and remove
  keyboard or mouse search steps.
- Every remaining step must be necessary for the final objective.
- The workflow does not contain controller names, plugin names, MCP names, or
  Python class names.
- No target is ApplicationController, BrowserController, DesktopController,
  WindowController, KeyboardController, MouseController, ClipboardController,
  FileController, BrowserPlugin, DesktopPlugin, FilesystemPlugin, ShellPlugin,
  Browser MCP, Desktop MCP, Filesystem MCP, or Terminal MCP.
- Filesystem-only tasks do not contain open_application.

If validation fails, regenerate the JSON before responding.
If the workflow contains unnecessary steps, remove them and renumber ids before
returning JSON.

==================================================
TASK
==================================================

{command}
"""




        try:

            response = (
                self.provider_manager
                .execute(
                    task_type="workflow_planning",
                    prompt=prompt
                )
            )

            if isinstance(response, str):
                try:
                    workflow = json.loads(response)
                except json.JSONDecodeError:
                    print("[WORKFLOW ERROR] Invalid JSON returned by planner.")
                    print(response)
                    return []
            else:
                workflow = response

            print("\n========== GENERATED WORKFLOW ==========")
            print(workflow)
            print("========================================\n")

            # Support both:
            # 1. [...]
            # 2. {"workflow": [...]}

            if isinstance(workflow, dict):
                workflow = workflow.get("workflow", [])

            if isinstance(workflow, list):
                return self.validate_workflow(workflow)

        except Exception as e:

            print(
                f"[WORKFLOW ERROR] {e}"
            )

        return []

    def validate_workflow(
        self,
        workflow: list
    ) -> list[dict]:
        """
        Validate workflow.
        """

        allowed_actions = {

            "open_application",
            "focus_window",
            "wait_seconds",

            "type_text",
            "press_key",

            "move_mouse",
            "mouse_click",
            "double_click",

            "create_directory",
            "delete_directory",
            "create_file",

            "open_url",

            "git_status",
            "git_branch",

            "security_scan",

            "terminal_command",

            "database_execute_query",

            "browser_title",
            "browser_extract_text",
            
            "open_browser",
            "navigate_url",
            "browser_search",
            "new_tab",
            "close_tab",
            "refresh_browser",
            "browser_back",
            "browser_forward",
            "browser_history",
            "browser_downloads",
            "close_browser",
        }

        validated = []

        for step in workflow:

            action = (
                step.get(
                    "action"
                )
            )

            if (
                action
                in allowed_actions
            ):

                validated.append(
                    step
                )

        return validated

    def has_workflow(
        self,
        command: str
    ) -> bool:
        """
        Determine whether
        workflow planning
        is required.
        """

        command = (
            command.lower()
        )

      

        keywords = {
                # Browser
                "chrome",
                "firefox",
                "edge",
                "browser",
                "website",
                "url",
                "youtube",
                "google",

                # Desktop
                "notepad",
                "calculator",
                "window",
                "click",
                "mouse",
                "keyboard",
                "type",
                "press",

                # Filesystem
                # Filesystem
"folder",
"directory",
"file",
"document",
"text file",
"txt",
"pdf",
"csv",
"excel",
"word",

"create",
"delete",
"remove",
"rename",
"move",
"copy",
"duplicate",

"read",
"write",
"save",
"open file",

"mkdir",
"touch",

"path",
"drive",
"disk",

"c:\\",
"d:\\",
"e:\\",

"downloads",
"desktop",
"documents",
"pictures",
"videos",
"music",

"zip",
"extract",
"unzip",
"compress",
            }

        return any(keyword in command for keyword in keywords)

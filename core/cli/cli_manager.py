from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from core.agents.agent_manager import AgentManager
from core.agents.architect_agent import ArchitectAgent
from core.agents.coder_agent import CoderAgent
from core.agents.memory_agent import MemoryAgent
from core.agents.planner_agent import PlannerAgent
from core.agents.reviewer_agent import ReviewerAgent
from core.agents.tester_agent import TesterAgent
from core.automation.automation_engine import AutomationEngine
from core.automation.desktop_controller import DesktopController
from core.automation.desktop_session_manager import DesktopSessionManager
from core.cli.model_selector import ModelSelector
from core.context.context_pipeline import ContextPipeline
from core.context.document_parser import DocumentParser
from core.context.knowledge_manager import KnowledgeManager
from core.context.project_loader import ProjectLoader
from core.context.project_path_resolver import ProjectPathResolver
from core.execution.autonomous_execution_engine import AutonomousExecutionEngine
from core.execution.execution_engine_config import ExecutionEngineConfig
from core.executor.execution_pipeline import ExecutionPipeline
from core.healing.recursive_engine import RecursiveEngine
from core.logging.kairos_logger import KairosLogger
from core.pipeline.pipeline_context import PipelineContext
from core.pipeline.pipeline_executor import PipelineExecutor
from core.pipeline.pipeline_result import PipelineResult
from core.pipeline.pipeline_selector import PipelineSelector
from core.pipeline.software_engine import SoftwareEngine
from core.plugins.filesystem_plugin import FilesystemPlugin
from core.router.intent_handler import IntentHandler
from core.router.route_executor import RouteExecutor
from core.router.task_router import TaskRouter
from core.router.workflow_planner import WorkflowPlanner
from core.runtime.runtime_manager import RuntimeManager
from core.sandbox.sandbox_manager import SandboxManager
from core.validation.validation_pipeline import ValidationPipeline
from core.runtime.mode_manager import ModeManager


CommandHandler = Callable[[str], dict[str, Any]]


@dataclass(frozen=True)
class CLICommand:
    prefix: str
    handler: CommandHandler
    exact: bool = False

    def matches(self, command: str) -> bool:
        return command == self.prefix if self.exact else command.startswith(self.prefix)


class CLIManager:
    """Lightweight boundary that wires dependencies and delegates execution."""

    SOFTWARE_ATTRIBUTES = {
        "pipeline_executor",
        "pipeline_selector",
        "project_loader",
        "document_parser",
        "knowledge_manager",
        "context_pipeline",
        "project_path_resolver",
        "validation",
        "execution",
        "healing",
        "generated_workspace",
    }

    def __init__(
        self,
        *,
        agent_manager: AgentManager | None = None,
        planner: PlannerAgent | None = None,
        architect: ArchitectAgent | None = None,
        coder: CoderAgent | None = None,
        reviewer: ReviewerAgent | None = None,
        tester: TesterAgent | None = None,
        memory_agent: MemoryAgent | None = None,
        runtime: RuntimeManager | None = None,
        filesystem: FilesystemPlugin | None = None,
        sandbox: SandboxManager | None = None,
        desktop: DesktopController | None = None,
        desktop_session: DesktopSessionManager | None = None,
        task_router: TaskRouter | None = None,
        intent_handler: IntentHandler | None = None,
        route_executor: RouteExecutor | None = None,
        workflow_planner: WorkflowPlanner | None = None,
        project_loader: ProjectLoader | None = None,
        document_parser: DocumentParser | None = None,
        knowledge_manager: KnowledgeManager | None = None,
        context_pipeline: ContextPipeline | None = None,
        project_path_resolver: ProjectPathResolver | None = None,
        validation: ValidationPipeline | None = None,
        execution: ExecutionPipeline | None = None,
        healing: RecursiveEngine | None = None,
        model_selector: ModelSelector | None = None,
        pipeline_selector: PipelineSelector | None = None,
        pipeline_executor: PipelineExecutor | None = None,
        automation_engine: AutomationEngine | None = None,
        software_engine: SoftwareEngine | None = None,
        autonomous_execution_engine: AutonomousExecutionEngine | None = None,
        execution_config: ExecutionEngineConfig | None = None,
        generated_workspace: str | None = None,
        logger: KairosLogger | None = None,
    ) -> None:
        self.logger = logger or KairosLogger("kairos")
        self.agent_manager = agent_manager or AgentManager()
        self.planner = planner or PlannerAgent()
        self.architect = architect or ArchitectAgent()
        self.coder = coder or CoderAgent()
        self.reviewer = reviewer or ReviewerAgent()
        self.tester = tester or TesterAgent()
        self.memory_agent = memory_agent or MemoryAgent()
        self.runtime = runtime or RuntimeManager()
        self.runtime.initialize()
        self.mode_manager = ModeManager()
        self.filesystem = filesystem or FilesystemPlugin()
        self.sandbox = sandbox or SandboxManager()
        self.desktop = desktop or DesktopController()
        self.desktop_session = desktop_session or DesktopSessionManager()
        self.task_router = task_router or TaskRouter()
        self.intent_handler = intent_handler or IntentHandler()
        self.route_executor = route_executor or RouteExecutor(
            self.filesystem,
            self.desktop,
            self.runtime,
        )
        self.workflow_planner = workflow_planner or WorkflowPlanner()
        self.automation_engine = automation_engine or AutomationEngine(
            workflow_planner=self.workflow_planner,
            intent_handler=self.intent_handler,
            route_executor=self.route_executor,
        )
        self.autonomous_execution_engine = (
            autonomous_execution_engine
            or AutonomousExecutionEngine(
                execution_config or ExecutionEngineConfig(),
                architect=self.architect,
                coder=self.coder,
                reviewer=self.reviewer,
                filesystem=self.filesystem,
            )
        )
        self.software_engine = software_engine or SoftwareEngine(
            planner=self.planner,
            architect=self.architect,
            coder=self.coder,
            reviewer=self.reviewer,
            tester=self.tester,
            memory_agent=self.memory_agent,
            filesystem=self.filesystem,
            runtime=self.runtime,
            project_loader=project_loader,
            document_parser=document_parser,
            knowledge_manager=knowledge_manager,
            context_pipeline=context_pipeline,
            project_path_resolver=project_path_resolver,
            validation=validation,
            execution=execution,
            healing=healing,
            pipeline_selector=pipeline_selector,
            pipeline_executor=pipeline_executor,
            autonomous_execution_engine=self.autonomous_execution_engine,
            generated_workspace=generated_workspace,
        )
        self.model_selector = model_selector or ModelSelector()
        self._commands = self._build_command_table()

    def __getattr__(self, name: str) -> Any:
        if name in self.SOFTWARE_ATTRIBUTES and "software_engine" in self.__dict__:
            return getattr(self.software_engine, name)

        raise AttributeError(f"{type(self).__name__!s} has no attribute {name!r}")

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.SOFTWARE_ATTRIBUTES and "software_engine" in self.__dict__:
            setattr(self.software_engine, name, value)
            return

        super().__setattr__(name, value)

    def process_command(self, command: str) -> dict[str, Any]:
        normalized = command.strip()

        if not normalized:
            return self._success("No command provided.")

        try:
            direct_result = self._dispatch_direct_command(normalized)

            if direct_result is not None:
                return direct_result

           # Generation Mode
            if self.mode_manager.is_generation():
                self.logger.info("Mode: Generation")
                return self.software_engine.execute(normalized)

            # Desktop Automation Mode
            self.logger.info("Mode: Desktop Automation")

            route = self.task_router.route(normalized)
            self.logger.info(f"Task Route: {route}")
            
            
            # Only allow automation routes
            if route in AutomationEngine.AUTOMATION_ROUTES:
                return self.automation_engine.execute(normalized, route)
            
            return {
                "status": "failed",
                "message": ( 
                    "Software generation is disabled in Desktop Automation Mode. "
                    "Switch to Generation Mode using /mode."),
              
                }
        except Exception as error:
            self.logger.error(f"Command failed: {error}")
            
            return {
        "status": "failed",
        "message": str(error),
    }

       
 
    def list_commands(self) -> list[str]:
        return sorted(command.prefix for command in self._commands)

    def list_pipelines(self) -> list[str]:
        return self.software_engine.list_pipelines()

    def set_generated_workspace(self, path: str) -> None:
        self.software_engine.set_generated_workspace(path)

    def build_pipeline_context(self, command: str) -> PipelineContext:
        return self.software_engine.build_pipeline_context(command)

    def select_pipeline(self, command: str) -> str:
        return self.software_engine.select_pipeline(command)

    def execute_pipeline(
        self,
        pipeline: str,
        context: PipelineContext,
        **kwargs: Any,
    ) -> PipelineResult:
        return self.software_engine.execute_pipeline(pipeline, context, **kwargs)

    def _build_command_table(self) -> list[CLICommand]:
        return [
            CLICommand("/help", lambda c: self._success(self.list_commands()), True),
            CLICommand("/status", lambda c: self._success("KAIROS Active"), True),
            CLICommand("/agents", lambda c: self._success(self.agent_manager.list_agents()), True),
            CLICommand("/mode", self._handle_mode, True),
            CLICommand("/memory", lambda c: self._success("Memory System Available"), True),
            CLICommand("/mcps", lambda c: self._success(self.runtime.mcp_server.list_tools()), True),
            CLICommand("/plugins", lambda c: self._success(self.runtime.plugin_manager.list_plugins()), True),
            CLICommand("/tools", self._handle_tools, True),
            CLICommand("/pipelines", lambda c: self._success(self.list_pipelines()), True),
            CLICommand("/terminal ", lambda c: self._plugin("TerminalPlugin", self._after(c, "/terminal "))),
            CLICommand("/git status", lambda c: self._plugin("GitPlugin", "status"), True),
            CLICommand("/git branch", lambda c: self._plugin("GitPlugin", "branch"), True),
            CLICommand("/security ", lambda c: self._plugin("SecurityPlugin", self._after(c, "/security "))),
            CLICommand("/doc ", self._handle_documentation_plugin),
            CLICommand("/browser ", lambda c: self._plugin("BrowserPlugin", self._after(c, "/browser "))),
            CLICommand("/browser-title ", lambda c: self._success(self._mcp("BrowserMCP").get_title(self._after(c, "/browser-title ")))),
            CLICommand("/browser-read ", lambda c: self._success(self._mcp("BrowserMCP").extract_text(self._after(c, "/browser-read ")))),
            CLICommand("/docker-status", lambda c: self._success(self._mcp("DockerMCP").is_connected()), True),
            CLICommand("/docker-containers", lambda c: self._success(self._mcp("DockerMCP").list_containers()), True),
            CLICommand("/docker-info ", lambda c: self._success(self._mcp("DockerMCP").get_container_info(self._after(c, "/docker-info ")))),
            CLICommand("/database-status", lambda c: self._success(self._mcp("DatabaseMCP").is_connected()), True),
            CLICommand("/database-query ", self._handle_database_query),
            CLICommand("/database-fetch ", lambda c: self._success(self._mcp("DatabaseMCP").fetch_one(self._after(c, "/database-fetch ")))),
            CLICommand("/github-status", lambda c: self._success(self._mcp("GitHubMCP").is_connected()), True),
            CLICommand("/github-repo ", lambda c: self._success(self._mcp("GitHubMCP").get_repository(self._after(c, "/github-repo ")))),
            CLICommand("/test ", lambda c: self._plugin("TestingPlugin", self._after(c, "/test "))),
            CLICommand("/file exists ", lambda c: self._plugin("FilesystemPlugin", "exists", self._after(c, "/file exists "))),
            CLICommand("/file read ", lambda c: self._plugin("FilesystemPlugin", "read", self._after(c, "/file read "))),
            CLICommand("/desktop-status", lambda c: self._success(self.desktop.get_status()), True),
            CLICommand("/windows", lambda c: self._success(self.desktop.window.get_window_titles()), True),
            CLICommand("/processes", lambda c: self._success(self.desktop.application.list_processes()), True),
            CLICommand("/mouse-position", self._handle_mouse_position, True),
            CLICommand("/open ", lambda c: self._success(self.desktop.launch_application(self._after(c, "/open ")))),
            CLICommand("/type ", self._handle_type_text),
            CLICommand("/press ", lambda c: self._success(self.desktop.press_key(self._after(c, "/press ")))),
            CLICommand("/focus ", lambda c: self._success(self.desktop.focus_window(self._after(c, "/focus ")))),
            CLICommand("/session", lambda c: self._success(self.desktop_session.get_active_window()), True),
            CLICommand("/mouse-move ", self._handle_mouse_move),
            CLICommand("/mouse-click", lambda c: self._success(self.desktop.mouse.click()), True),
            CLICommand("/mouse-double-click", lambda c: self._success(self.desktop.mouse.double_click()), True),
            CLICommand("/init-project ", self._handle_init_project),
            CLICommand("/create-dir ", self._handle_create_dir),
            CLICommand("/list-files ", self._handle_list_files),
            CLICommand("/read-file ", lambda c: self._success(self.filesystem.execute("read", self._after(c, "/read-file ")))),
            CLICommand("/write-file ", self._handle_write_file),
            CLICommand("/exists-file ", lambda c: self._success(str(self.filesystem.execute("exists", self._after(c, "/exists-file "))))),
            CLICommand("/delete-file ", self._handle_delete_file),
            CLICommand("/model", self._handle_model, True),
            CLICommand("/model-info", self._handle_model_info, True),
            CLICommand("/reset-model", self._handle_reset_model, True),
            CLICommand("/providers", lambda c: {"status": "success", "files": list(self.model_selector.get_providers().values())}, True),
            CLICommand("/models", self._handle_models, True),
        ]

    def _dispatch_direct_command(self, command: str) -> dict[str, Any] | None:
        for route in self._commands:
            if route.matches(command):
                return route.handler(command)

        return None

    def _handle_tools(self, command: str) -> dict[str, Any]:
        return {
            "status": "success",
            "mcps": self.runtime.mcp_server.list_tools(),
            "plugins": self.runtime.plugin_manager.list_plugins(),
        }

    def _handle_documentation_plugin(self, command: str) -> dict[str, Any]:
        action, project_name = self._after(command, "/doc ").split(" ", 1)

        return self._plugin("DocumentationPlugin", action, project_name)

    def _handle_database_query(self, command: str) -> dict[str, Any]:
        self._mcp("DatabaseMCP").execute_query(self._after(command, "/database-query "))

        return self._success("Query Executed")

    def _handle_mouse_position(self, command: str) -> dict[str, Any]:
        position = self.desktop.mouse.get_position()

        return self._success(f"X={position[0]} Y={position[1]}")

    def _handle_type_text(self, command: str) -> dict[str, Any]:
        self._focus_active_window()

        return self._success(self.desktop.keyboard.type_text(self._after(command, "/type ")))
    
    def _handle_mode(self, command: str) -> dict[str, Any]:
        print("\nSelect KAIROS Mode\n")
        print("1. Generation")
        print("2. Desktop Automation")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            confirm = input(
                "\nSwitch to Generation Mode? (Y/N): "
            ).strip().lower()

            if confirm == "y":
                self.mode_manager.set_mode("generation")
                return self._success("Active Mode: Generation")

            return self._success("Mode switch cancelled.")

        elif choice == "2":
            confirm = input(
                "\nSwitch to Desktop Automation Mode? (Y/N): "
            ).strip().lower()

            if confirm == "y":
                self.mode_manager.set_mode("desktop")
                return self._success("Active Mode: Desktop Automation")

            return self._success("Mode switch cancelled.")

        return {
            "status": "failed",
            "message": "Invalid selection."
        }

    def _handle_mouse_move(self, command: str) -> dict[str, Any]:
        parts = command.split()

        if len(parts) != 3:
            raise ValueError("Usage: /mouse-move <x> <y>")

        return self._success(self.desktop.mouse.move_mouse(int(parts[1]), int(parts[2])))

    def _handle_init_project(self, command: str) -> dict[str, Any]:
        path = self._after(command, "/init-project ")
        self.filesystem.execute("init_project", path)

        return self._success(f"KAIROS project initialized at {path}")

    def _handle_create_dir(self, command: str) -> dict[str, Any]:
        path = self._after(command, "/create-dir ")
        self.filesystem.execute("create_directory", path)

        return self._success(f"Directory created: {path}")

    def _handle_list_files(self, command: str) -> dict[str, Any]:
        return {
            "status": "success",
            "files": self.filesystem.execute("list_directory", self._after(command, "/list-files ")),
        }

    def _handle_write_file(self, command: str) -> dict[str, Any]:
        path, content = self._after(command, "/write-file ").split("|", 1)
        self.filesystem.execute("write", path, content)

        return self._success(f"File written: {path}")

    def _handle_delete_file(self, command: str) -> dict[str, Any]:
        path = self._after(command, "/delete-file ")
        self.filesystem.execute("delete", path)

        return self._success(f"File deleted: {path}")

    def _handle_model(self, command: str) -> dict[str, Any]:
        session = self.model_selector.load_session()

        if session:
            print("\nCurrent Session\n")
            print(f"Provider: {session['provider']}")
            print(f"Model: {session['model']}")

        if input("\nChange model? (y/n): ").lower() == "y":
            self.model_selector.configure()

        return self._success("Model updated.")

    def _handle_model_info(self, command: str) -> dict[str, Any]:
        session = self.model_selector.load_session()

        return self._success(f"Provider: {session['provider']}\nModel: {session['model']}")

    def _handle_reset_model(self, command: str) -> dict[str, Any]:
        session_file = Path(".kairos/session.json")

        if session_file.exists():
            session_file.unlink()

        return self._success("Model session reset.")

    def _handle_models(self, command: str) -> dict[str, Any]:
        session = self.model_selector.load_session()

        return {
            "status": "success",
            "files": list(self.model_selector.get_models(session["provider"]).values()),
        }

    def _focus_active_window(self) -> None:
        active_window = self.desktop_session.get_active_window()

        if active_window:
            self.desktop.window.focus_window(active_window)

    def _plugin(self, name: str, *args: Any) -> dict[str, Any]:
        return self._success(self.runtime.plugin_manager.get_plugin(name).execute(*args))

    def _mcp(self, name: str) -> Any:
        return self.runtime.mcp_server.get_tool(name)

    def _after(self, command: str, prefix: str) -> str:
        return command.replace(prefix, "", 1).strip()

    def _success(self, message: Any) -> dict[str, Any]:
        return {
            "status": "success",
            "message": message,
        }

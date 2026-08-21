"""
Autonomous Execution Engine.

The AutonomousExecutionEngine is the central orchestrator of KAIROS.

Responsibilities
----------------
- Receive execution requests
- Discover the workspace
- Understand the repository
- Build an execution plan
- Select the appropriate agent
- Coordinate execution
- Track execution lifecycle
- Return execution results

This class NEVER contains business logic for:

- Repository analysis
- Planning
- Code generation
- Tool implementations

Those responsibilities belong to dedicated components.


FLOW : 

User Request
      │
      ▼
AutonomousExecutionEngine
      │
      ├──────────────┐
      ▼              │
WorkspaceDiscovery   │
      ▼              │
RepositoryUnderstanding
      ▼
ExecutionPlanner
      ▼
ExecutionContext
      ▼
Agent Selection
      ▼
ArchitectAgent / CoderAgent / ReviewerAgent
      ▼
ExecutionResult

"""

from __future__ import annotations

from pathlib import Path

from .execution_engine_config import ExecutionEngineConfig
from .execution_planner import ExecutionPlanner
from .repository_understanding import RepositoryUnderstanding
from .workspace_discovery import WorkspaceDiscovery

from ..agents.architect_agent import ArchitectAgent
from ..agents.coder_agent import CoderAgent
from ..agents.reviewer_agent import ReviewerAgent
from ..logging.kairos_logger import KairosLogger
from ..orchestration.agent_coordinator import AgentCoordinator
from ..orchestration.execution_loop import ExecutionLoop
from ..plugins.filesystem_plugin import FilesystemPlugin

from ..execution.execution_result import ExecutionResult
from .context_builder import ContextBuilder

class AutonomousExecutionEngine:
    """
    Central orchestration engine.

    Coordinates every execution phase while delegating
    actual work to specialized components.
    """

    def __init__(
        self,
        config: ExecutionEngineConfig,
        *,
        workspace_discovery: WorkspaceDiscovery | None = None,
        repository_understanding: RepositoryUnderstanding | None = None,
        execution_planner: ExecutionPlanner | None = None,
        context_builder: ContextBuilder | None = None,
        architect: ArchitectAgent | None = None,
        coder: CoderAgent | None = None,
        reviewer: ReviewerAgent | None = None,
        execution_loop: ExecutionLoop | None = None,
        filesystem: FilesystemPlugin | None = None,
        logger: KairosLogger | None = None,
    ) -> None:

        self._config = config
        self._logger = logger or KairosLogger("execution")
        self._filesystem = filesystem or FilesystemPlugin()

        self._workspace_discovery = (
            workspace_discovery
            or WorkspaceDiscovery()
        )

        self._repository_understanding = (
            repository_understanding
            or RepositoryUnderstanding()
        )

        self._execution_planner = (
            execution_planner
            or ExecutionPlanner()
        )

        self._architect = (
            architect
            or ArchitectAgent()
        )

        self._coder = (
            coder
            or CoderAgent()
        )

        self._reviewer = (
            reviewer
            or ReviewerAgent()
        )
        
        self._context_builder = (
            context_builder
            or ContextBuilder()
        )

        self._agent_coordinator = AgentCoordinator(
            architect=self._architect,
            coder=self._coder,
            reviewer=self._reviewer,
        )

        self._execution_loop = (
            execution_loop
            or ExecutionLoop(
                coordinator=self._agent_coordinator,
                config=self._config,
                filesystem=self._filesystem,
            )
        )

    
        
    
    def _validate_execution_request(
        self,
        task: str,
        workspace: str | Path,
    ) -> None:
        """
        Validate an execution request.
        """

        if not task:
            raise ValueError("Task cannot be empty.")

        if not workspace:
            raise ValueError("Workspace cannot be empty.")

    def _prepare_execution(
        self,
        *,
        task: str,
        workspace: str | Path,
    ):
        """
        Perform all preparation steps before execution.

        Returns
        -------
        tuple
            WorkspaceResult,
            RepositoryResult,
            ExecutionContext
        """

        workspace_result = (
            self._workspace_discovery.discover(
                workspace
            )
        )

        repository_result = (
            self._repository_understanding.analyze(
                workspace_result.workspace
            )
        )

        execution_context = (
            self._execution_planner.plan(
                task=task,
                workspace=workspace_result,
                repository=repository_result,
                config=self._config,
            )
        )

        return (
            workspace_result,
            repository_result,
            execution_context,
        )

    def _execute_plan(
        self,
        execution_context,
    ):
        """
        Execute a prepared plan.
        """
        
        agent_context = self._context_builder.build(
            execution_context=execution_context,
            config=self._config,
        )

        return self._execution_loop.run(
            execution_context=execution_context,
            agent_context=agent_context,
        )

    def _finalize_execution(
        self,
        execution_context,
        agent_result,
    ) -> ExecutionResult:
        """
        Finalize execution and build the final result.
        """

        return agent_result
        
    
    def _build_result(
        self,
        execution_context,
        agent_result,
    ) -> ExecutionResult:
        """
        Build the final execution result.
        """

        return ExecutionResult(
            task=execution_context.task,
            task_type=execution_context.task_type,
            complexity=execution_context.complexity,
            repository=execution_context.repository,
            success=agent_result.success,
            message=agent_result.message,
            output=agent_result.output,
            artifacts=agent_result.artifacts,
            metadata=agent_result.metadata,
        )

    def execute(
        self,
        *,
        task: str,
        workspace: str | Path,
    ) -> ExecutionResult:
        """
        Execute a user request.

        This is the public entry point into the KAIROS execution engine.
        """

        self._validate_execution_request(
            task,
            workspace,
        )

        try:
            (
                _,
                _,
                execution_context,
            ) = self._prepare_execution(
                task=task,
                workspace=workspace,
            )

            agent_result = self._execute_plan(
                execution_context,
            )

            return self._finalize_execution(
                execution_context,
                agent_result,
            )
        except Exception as exc:
            self._logger.error(
                f"Execution failed: {exc}"
            )

            return ExecutionResult(
                success=False,
                task=task,
                message=str(exc),
                metadata={
                    "error_type": type(exc).__name__,
                },
            )

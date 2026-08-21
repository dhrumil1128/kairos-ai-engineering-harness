from __future__ import annotations

from pathlib import Path, PureWindowsPath
from typing import Any

from core.agents.architect_agent import ArchitectAgent
from core.agents.coder_agent import CoderAgent
from core.agents.memory_agent import MemoryAgent
from core.agents.planner_agent import PlannerAgent
from core.agents.reviewer_agent import ReviewerAgent
from core.agents.tester_agent import TesterAgent
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
from core.plugins.filesystem_plugin import FilesystemPlugin
from core.runtime.runtime_manager import RuntimeManager
from core.validation.validation_pipeline import ValidationPipeline


class SoftwareEngine:
    """Owns project context, knowledge, pipeline selection, and execution."""

    GENERATED_DIRECTORY_NAME = "generated"

    def __init__(
        self,
        *,
        planner: PlannerAgent,
        architect: ArchitectAgent,
        coder: CoderAgent,
        reviewer: ReviewerAgent,
        tester: TesterAgent,
        memory_agent: MemoryAgent,
        filesystem: FilesystemPlugin,
        runtime: RuntimeManager,
        project_loader: ProjectLoader | None = None,
        document_parser: DocumentParser | None = None,
        knowledge_manager: KnowledgeManager | None = None,
        context_pipeline: ContextPipeline | None = None,
        project_path_resolver: ProjectPathResolver | None = None,
        validation: ValidationPipeline | None = None,
        execution: ExecutionPipeline | None = None,
        healing: RecursiveEngine | None = None,
        pipeline_selector: PipelineSelector | None = None,
        pipeline_executor: PipelineExecutor | None = None,
        autonomous_execution_engine: AutonomousExecutionEngine | None = None,
        execution_config: ExecutionEngineConfig | None = None,
        generated_workspace: str | None = None,
        logger: KairosLogger | None = None,
    ) -> None:
        self.planner = planner
        self.architect = architect
        self.coder = coder
        self.reviewer = reviewer
        self.tester = tester
        self.memory_agent = memory_agent
        self.filesystem = filesystem
        self.runtime = runtime
        self.project_loader = project_loader or ProjectLoader()
        self.document_parser = document_parser or DocumentParser()
        self.knowledge_manager = knowledge_manager or KnowledgeManager()
        self.context_pipeline = context_pipeline or ContextPipeline()
        self.project_path_resolver = project_path_resolver or ProjectPathResolver()
        self.validation = validation or ValidationPipeline()
        self.execution = execution or ExecutionPipeline()
        self.healing = healing or RecursiveEngine()
        self.pipeline_selector = pipeline_selector or PipelineSelector()
        self.pipeline_executor = pipeline_executor or PipelineExecutor()
        self.generated_workspace = generated_workspace
        self.logger = logger or KairosLogger("software")
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
        self._configure_pipeline_executor()

    def execute(self, command: str, **kwargs: Any) -> dict[str, Any]:
        context = self.build_pipeline_context(command)
        self.logger.info("Selected Pipeline: autonomous_execution")

        result = self.autonomous_execution_engine.execute(
            task=command,
            workspace=context.target_project,
        )

        return result.to_dict()

    def list_pipelines(self) -> list[str]:
        return self.pipeline_executor.list_pipelines()

    def set_generated_workspace(self, path: str) -> None:
        if not path.strip():
            raise ValueError("Generated workspace path cannot be blank.")

        self.generated_workspace = path.strip()

    def build_pipeline_context(self, command: str) -> PipelineContext:
        target_project = self.project_path_resolver.resolve(command)
        generated_project = self._resolve_generated_workspace(target_project)
        shared_context = self._build_shared_context(command, target_project)

        return PipelineContext(
            command=command,
            target_project=target_project,
            generated_project=generated_project,
            shared_context=shared_context,
        )

    def select_pipeline(self, command: str) -> str:
        return self.pipeline_selector.select(command)

    def execute_pipeline(
        self,
        pipeline: str,
        context: PipelineContext,
        **kwargs: Any,
    ) -> PipelineResult:
        return self.pipeline_executor.execute(
            pipeline,
            context=context,
            **kwargs,
        )

    def _configure_pipeline_executor(self) -> None:
        self.pipeline_executor.configure(
            planner=self.planner,
            architect=self.architect,
            memory_agent=self.memory_agent,
            coder=self.coder,
            reviewer=self.reviewer,
            tester=self.tester,
            healing=self.healing,
            filesystem=self.filesystem,
            validation_pipeline=self.validation,
            execution_pipeline=self.execution,
        )

    def _build_shared_context(
        self,
        command: str,
        target_project: str,
    ) -> dict[str, Any]:
        self.context_pipeline.clear()
        self.knowledge_manager.clear()

        if not self.project_loader.validate_project(target_project):
            return {
                "metadata": {},
                "documents": {},
                "knowledge": {},
                "ranked_context": [],
                "summary": {},
            }

        metadata = self.project_loader.load_project(target_project)
        self.context_pipeline.project_context.set_metadata(metadata)

        for document_name, document_content in metadata["documents"].items():
            parsed = self.document_parser.parse(document_content)
            self.context_pipeline.add_document(document_name, parsed)
            self.knowledge_manager.store(document_name, parsed)

        self.context_pipeline.project_context.set_knowledge(
            self.knowledge_manager.build_index()
        )

        shared_context = self.context_pipeline.build_context()
        shared_context["summary"] = self.context_pipeline.summary()
        shared_context["ranked_context"] = self.context_pipeline.rank_context(
            command,
            top_k=5,
        )

        self.logger.info(f"Target Project: {target_project}")
        self.logger.info(f"Context Summary: {shared_context['summary']}")

        return shared_context

    def _resolve_generated_workspace(self, target_project: str) -> str:
        if self.generated_workspace:
            return self.generated_workspace

        active_project = self.runtime.get_active_project()
        target_path = Path(target_project)

        if self._is_absolute(target_project):
            if not active_project:
                return str(target_path)

            active_path = Path(active_project)

            if target_path.resolve() != active_path.resolve():
                return str(target_path)

        project_root = Path(active_project or target_project)

        return str(project_root / ".kairos" / self.GENERATED_DIRECTORY_NAME)

    def _is_absolute(self, path: str) -> bool:
        return (
            Path(path).is_absolute()
            or PureWindowsPath(path).is_absolute()
        )

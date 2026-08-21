from __future__ import annotations

from typing import Any

from core.execution.execution_result import ExecutionResult
from core.healing.error_analyzer import ErrorAnalyzer
from core.healing.retry_manager import RetryManager
from core.healing.self_correction import SelfCorrection
from core.logging.kairos_logger import KairosLogger
from core.pipeline.path_resolution import resolve_output_path
from core.pipeline.pipeline_context import PipelineContext
from core.pipeline.sandbox_pipeline import SandboxPipeline
from core.plugins.filesystem_plugin import FilesystemPlugin

from .agent_coordinator import AgentCoordinator
from .repair_loop import RepairLoop


class ExecutionLoop:
    """
    Orchestrates the Architect, Coder, Reviewer lifecycle.
    """

    def __init__(
        self,
        *,
        coordinator: AgentCoordinator | None = None,
        config=None,
        filesystem: FilesystemPlugin | None = None,
        sandbox_pipeline: SandboxPipeline | None = None,
        logger: KairosLogger | None = None,
    ) -> None:
        self._coordinator = coordinator
        self._config = config
        self._filesystem = filesystem or FilesystemPlugin()
        self._sandbox_pipeline = sandbox_pipeline or SandboxPipeline(
            self._filesystem
        )
        self._logger = logger or KairosLogger("orchestration")

        self.error_analyzer = ErrorAnalyzer()
        self.retry_manager = RetryManager()
        self.self_correction = SelfCorrection()

    def run(
        self,
        *,
        execution_context,
        agent_context,
    ) -> ExecutionResult:
        if self._coordinator is None:
            raise ValueError(
                "ExecutionLoop requires an AgentCoordinator to run the agent lifecycle."
            )

        try:
            lifecycle = self._coordinator.run_lifecycle(
                agent_context,
            )

            if lifecycle["success"]:
                written_files = self._persist_implementation(
                    execution_context=execution_context,
                    implementation=lifecycle["implementation"],
                )
                lifecycle["written_files"] = written_files

                sandbox_result = self._run_sandbox(
                    execution_context=execution_context,
                    orchestration_result=lifecycle,
                )
                lifecycle["sandbox"] = sandbox_result.to_dict()

                if not sandbox_result.success:
                    lifecycle["success"] = False
                    return self._build_result(
                        execution_context=execution_context,
                        orchestration_result=lifecycle,
                        message="Review passed but sandbox execution failed.",
                    )

                return self._build_result(
                    execution_context=execution_context,
                    orchestration_result=lifecycle,
                    message="Execution completed successfully.",
                )

            if not getattr(self._config, "auto_repair", True):
                return self._build_result(
                    execution_context=execution_context,
                    orchestration_result=lifecycle,
                    message="Review failed and auto repair is disabled.",
                )

            repaired = RepairLoop(
                coordinator=self._coordinator,
                config=self._config,
                logger=self._logger,
            ).run(
                agent_context=lifecycle["agent_context"],
                implementation=lifecycle["implementation"],
                review=lifecycle["review"],
            )

            orchestration_result = {
                **lifecycle,
                **repaired,
                "architecture": lifecycle["architecture"],
            }

            if orchestration_result["success"]:
                written_files = self._persist_implementation(
                    execution_context=execution_context,
                    implementation=orchestration_result["implementation"],
                )
                orchestration_result["written_files"] = written_files

                sandbox_result = self._run_sandbox(
                    execution_context=execution_context,
                    orchestration_result=orchestration_result,
                )
                orchestration_result["sandbox"] = sandbox_result.to_dict()

                if not sandbox_result.success:
                    orchestration_result["success"] = False
                    return self._build_result(
                        execution_context=execution_context,
                        orchestration_result=orchestration_result,
                        message="Repair passed review but sandbox execution failed.",
                    )

            return self._build_result(
                execution_context=execution_context,
                orchestration_result=orchestration_result,
                message=repaired["message"],
            )

        except Exception as exc:
            self._logger.error(
                f"Execution loop failed: {exc}"
            )

            return ExecutionResult(
                success=False,
                task=getattr(execution_context, "task", None),
                task_type=getattr(execution_context, "task_type", None),
                complexity=getattr(execution_context, "complexity", None),
                repository=getattr(execution_context, "repository", None),
                message=str(exc),
                metadata={
                    "error_type": type(exc).__name__,
                },
            )

    def process_error(
        self,
        error_message: str,
        attempt: int,
    ) -> dict[str, Any]:
        if not self.retry_manager.should_retry(
            attempt,
        ):
            return {
                "status": "failed",
                "reason": "Retry limit reached",
            }

        analysis = self.error_analyzer.analyze(
            error_message,
        )
        repair_plan = self.self_correction.generate_fix(
            analysis,
        )

        return {
            "status": "retry",
            "analysis": analysis,
            "repair_plan": repair_plan,
            "review_required": True,
            "test_required": True,
            "validation_steps": repair_plan.get(
                "validation_steps",
                [],
            ),
            "attempt": attempt + 1,
            "max_retries": self.retry_manager.get_max_retries(),
        }

    def _build_result(
        self,
        *,
        execution_context,
        orchestration_result: dict[str, Any],
        message: str,
    ) -> ExecutionResult:
        implementation = orchestration_result.get("implementation")
        review = orchestration_result.get("review")

        return ExecutionResult(
            success=bool(orchestration_result.get("success")),
            task=execution_context.task,
            task_type=execution_context.task_type,
            complexity=execution_context.complexity,
            repository=execution_context.repository,
            message=message,
            output=implementation,
            artifacts=self._artifacts(implementation),
            metadata={
                "architecture": self._serialize_architecture(
                    orchestration_result.get("architecture"),
                ),
                "review": review,
                "repair_attempts": orchestration_result.get("attempts", 0),
                "written_files": orchestration_result.get(
                    "written_files",
                    [],
                ),
                "sandbox": orchestration_result.get("sandbox"),
            },
            data={
                "implementation": implementation,
                "review": review,
            },
        )

    def _run_sandbox(
        self,
        *,
        execution_context,
        orchestration_result: dict[str, Any],
    ):
        if not getattr(self._config, "verify_after_execution", True):
            return _SkippedSandboxResult()

        workspace_root = self._workspace_root(
            execution_context,
        )

        pipeline_context = PipelineContext(
            command=str(execution_context.task),
            target_project=workspace_root,
            generated_project=workspace_root,
            shared_context={},
        )

        architecture = self._serialize_architecture(
            orchestration_result.get("architecture"),
        )

        return self._sandbox_pipeline.execute(
            context=pipeline_context,
            architecture=architecture or {},
            implementation=orchestration_result.get("implementation") or {},
        )

    def _persist_implementation(
        self,
        *,
        execution_context,
        implementation: dict[str, Any],
    ) -> list[str]:
        if not getattr(self._config, "enable_file_tools", True):
            raise RuntimeError(
                "Generated files cannot be written because file tools are disabled."
            )

        files = self._implementation_files(
            implementation,
        )

        if not files:
            raise ValueError(
                "Generated implementation does not contain files to write."
            )

        workspace_root = self._workspace_root(
            execution_context,
        )
        written_files: list[str] = []

        for file in files:
            path = file.get("path")
            content = file.get("content")

            if not path:
                raise ValueError(
                    "Generated file is missing a path."
                )

            if content is None:
                raise ValueError(
                    f"Generated file is missing content: {path}"
                )

            output_path = resolve_output_path(
                workspace_root,
                str(path),
            )

            self._filesystem.execute(
                "write",
                output_path,
                str(content),
            )

            written_files.append(
                output_path,
            )
            self._logger.debug(
                f"Wrote generated file: {output_path}"
            )

        return written_files

    def _implementation_files(
        self,
        implementation: dict[str, Any],
    ) -> list[dict[str, Any]]:
        if not isinstance(
            implementation,
            dict,
        ):
            return []

        files = implementation.get(
            "implementation_spec",
            {},
        ).get(
            "files",
            [],
        )

        if not isinstance(
            files,
            list,
        ):
            return []

        return [
            file
            for file in files
            if isinstance(
                file,
                dict,
            )
        ]

    def _workspace_root(
        self,
        execution_context,
    ) -> str:
        workspace = getattr(
            execution_context,
            "workspace",
            None,
        )

        path = getattr(
            workspace,
            "path",
            None,
        )

        if path:
            return str(path)

        if isinstance(
            workspace,
            str,
        ):
            return workspace

        raise ValueError(
            "Execution context does not contain a writable workspace path."
        )

    def _artifacts(
        self,
        implementation: Any,
    ) -> list[Any]:
        if not isinstance(implementation, dict):
            return []

        return list(
            implementation.get(
                "implementation_spec",
                {},
            ).get(
                "files",
                [],
            )
        )

    def _serialize_architecture(
        self,
        architecture: Any,
    ) -> Any:
        if hasattr(architecture, "to_dict"):
            return architecture.to_dict()

        return architecture


class _SkippedSandboxResult:
    success = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": "skipped",
            "success": True,
            "reason": "verify_after_execution is disabled.",
        }

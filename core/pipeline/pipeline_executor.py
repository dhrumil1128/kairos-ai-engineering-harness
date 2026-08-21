"""
File:
core/pipeline/pipeline_executor.py

Purpose:
Execute selected pipelines
and orchestrate the complete
software workflow.

Why:

PipelineExecutor is the
runtime boundary between
CLI selection and workflow
execution.

Simple pipelines can still
be executed directly by
name.  Generation, however,
is a full software workflow
because code generation
depends on analysis output
and later stages depend on
generated implementation
state.

Responsibilities:

- Configure pipelines.
- Register pipelines.
- Route execution requests.
- Orchestrate software
  workflow order.
- Isolate repair handling.
- Return standardized
  PipelineResult objects.

Does NOT:

- Decide which pipeline
  should run.
- Perform AI tasks.
- Generate code directly.
- Analyze projects directly.
- Leak workflow order into
  CLIManager.

Architecture:

CLI Manager
      |
      v
Pipeline Selector
      |
      v
Pipeline Executor
      |
      +-- Analysis Pipeline
      +-- Documentation Pipeline
      +-- Generation Pipeline
      +-- Validation Pipeline
      +-- Execution Pipeline
      +-- Review Pipeline
      +-- Testing Pipeline
      +-- Repair Pipeline
"""

from __future__ import annotations

from typing import Any

from core.logging.kairos_logger import (
    KairosLogger
)



from core.pipeline.repair_pipeline import (
    RepairPipeline
)

from core.pipeline.review_pipeline import (
    ReviewPipeline
)

from core.pipeline.testing_pipeline import (
    TestingPipeline
)

from core.pipeline.sandbox_pipeline import (
    SandboxPipeline
)

from core.pipeline.healing_pipeline import (
    HealingPipeline
)

from core.pipeline.documentation_pipeline import (
    DocumentationPipeline
)

from core.pipeline.pipeline_result import (
    PipelineResult
)

from core.validation.validation_pipeline import (
    ValidationPipeline
)

from core.executor.execution_pipeline import (
    ExecutionPipeline
)

from core.architecture.blueprint import ArchitectureBlueprint

class PipelineExecutor:
    """
    Execute registered
    pipelines and orchestrate
    production workflows.
    """

    SOFTWARE_WORKFLOW_PIPELINE = "generation"

    def __init__(self):
        """
        Initialize executor.
        """
        self.logger = KairosLogger("pipeline")
        self._pipelines = {}

        # Pipeline instances
        self.analysis_pipeline = None
        self.generation_pipeline = None
        self.repair_pipeline = None
        self.review_pipeline = None
        self.testing_pipeline = None
        self.sandbox_pipeline = None
        self.healing_pipeline = None
        self.documentation_pipeline = None
        self.validation_pipeline = None
        self.execution_pipeline = None

    # ----------------------------------
    # Configure Pipelines
    # ----------------------------------

    def configure(
        self,
        *,
        planner,
        architect,
        memory_agent,
        coder,
        reviewer,
        tester,
        healing,
        filesystem,
        validation_pipeline=None,
        execution_pipeline=None
    ) -> None:
        """
        Configure every pipeline.

        Why:

        The PipelineExecutor
        should not create
        agent dependencies itself.

        Instead, CLIManager
        injects them once,
        following the Dependency
        Injection principle.
        """

        # Creating the filesystem dependency
        self.filesystem = filesystem
       

        # --------------------------
        # Repair Pipeline
        # --------------------------
        self.repair_pipeline = RepairPipeline(
            healing,
            coder,
            filesystem
        )

        # --------------------------
        # Review Pipeline
        # --------------------------
        self.review_pipeline = ReviewPipeline(
            reviewer
        )

        # --------------------------
        # Testing Pipeline
        # --------------------------
        self.testing_pipeline = TestingPipeline(
            tester
        )

        self.sandbox_pipeline = SandboxPipeline(
            filesystem
        )

        # --------------------------
        # Documentation Pipeline
        # --------------------------
        self.documentation_pipeline = DocumentationPipeline(
            memory_agent
        )

        # --------------------------
        # Validation Pipeline
        # --------------------------
        self.validation_pipeline = (
            validation_pipeline
            or ValidationPipeline()
        )

        self.healing_pipeline = HealingPipeline(
            healing,
            coder,
            filesystem,
            validation_pipeline=self.validation_pipeline,
            sandbox_pipeline=self.sandbox_pipeline
        )

        # --------------------------
        # Execution Pipeline
        # --------------------------
        self.execution_pipeline = (
            execution_pipeline
            or ExecutionPipeline()
        )

        # Register default pipelines
        self.register_default_pipelines()

    # ----------------------------------
    # Register Default Pipelines
    # ----------------------------------

    def register_default_pipelines(self) -> None:
        """
        Register every built-in pipeline.

        Why:

        Centralizes pipeline
        registration in one
        place.

        Called once after
        configure().
        """
        if self.analysis_pipeline:
            self.register(
                self.analysis_pipeline.name,
                self.analysis_pipeline
            )

        if self.generation_pipeline:
            self.register(
                self.generation_pipeline.name,
                self.generation_pipeline
            )

        if self.repair_pipeline:
            self.register(
                self.repair_pipeline.name,
                self.repair_pipeline
            )

        if self.review_pipeline:
            self.register(
                self.review_pipeline.name,
                self.review_pipeline
            )

        if self.testing_pipeline:
            self.register(
                self.testing_pipeline.name,
                self.testing_pipeline
            )

        if self.sandbox_pipeline:
            self.register(
                self.sandbox_pipeline.name,
                self.sandbox_pipeline
            )

        if self.healing_pipeline:
            self.register(
                self.healing_pipeline.name,
                self.healing_pipeline
            )

        if self.documentation_pipeline:
            self.register(
                self.documentation_pipeline.name,
                self.documentation_pipeline
            )

        if self.validation_pipeline:
            self.register(
                "validation",
                self.validation_pipeline
            )

        if self.execution_pipeline:
            self.register(
                "execution",
                self.execution_pipeline
            )

    # ----------------------------------
    # Register Pipeline
    # ----------------------------------

    def register(
        self,
        name: str,
        pipeline: object  # BasePipeline will replace 'object' in a later refactor.
    ) -> None:
        """
        Register a pipeline.

        Why:

        Stores the pipeline
        so it can be executed
        later by name.
        """

        if name in self._pipelines:

            raise ValueError(

                f"Pipeline '{name}' is already registered."

            )

        # Store the pipeline
        # instance for future
        # execution.
        self._pipelines[
            name
        ] = pipeline

    # ----------------------------------
    # Has Pipeline
    # ----------------------------------

    def has_pipeline(
        self,
        name: str
    ) -> bool:
        """
        Check whether a
        pipeline has been
        registered.

        Why:

        Prevents execution
        of unknown pipelines
        and allows safe
        existence checks.
        """

        return (

            name in self._pipelines

        )

    # ----------------------------------
    # Get Pipeline
    # ----------------------------------

    def get_pipeline(
        self,
        name: str
    ) -> object:  # BasePipeline will replace 'object' in a later refactor.
        """
        Return a registered
        pipeline instance.

        Why:

        Some modules need
        direct access to a
        pipeline without
        executing it.
        """

        if not self.has_pipeline(
            name
        ):

            raise ValueError(

                f"Pipeline '{name}' is not registered."

            )

        # Return the requested
        # pipeline instance.
        return self._pipelines[
            name
        ]

    # ----------------------------------
    # Execute Pipeline
    # ----------------------------------

    def execute(
        self,
        name: str,
        **kwargs  # Forward named arguments to the selected pipeline.
    ) -> PipelineResult:
        """
        Route the requested
        pipeline execution.

        Why:

        Generation is no longer
        a single isolated stage.
        It represents the complete
        software workflow, so this
        public method remains a
        router while private methods
        own orchestration details.

        Raises:

        ValueError if a direct
        pipeline is not registered.
        """

        self.logger.info(
            f"Executing Pipeline: {name}"
        )

        if name == self.SOFTWARE_WORKFLOW_PIPELINE:
            return self._execute_software_workflow(
                **kwargs
            )

        pipeline = (
            self.get_pipeline(
                name
            )
        )

        return pipeline.execute(
            **kwargs
        )

    # ------------------------------------------------------------------
    # Software Workflow Orchestration
    # ------------------------------------------------------------------

    def _execute_software_workflow(
        self,
        **kwargs: Any
    ) -> PipelineResult:
        """
        Execute the complete
        software workflow.

        Order:

        1. Analysis
        2. Documentation
        3. Generation
        4. Validation
        5. Execution
        6. Review
        7. Testing

        Repair is intentionally
        isolated and invoked only
        after validation or
        execution failure.
        """

        context = (
            kwargs.get(
                "context"
            )
        )
        
        target_project = getattr(
            context,
            "generated_project",
            None
        )

        if target_project:

            target_project = self.filesystem.execute(
                "prepare_project",
                target_project
            )

            context.generated_project = str(
                target_project
            )
            
    

        if context is None:
            return self._workflow_failure(
                "generation",
                "PipelineContext is required for software workflow."
            )

        workflow_data: dict[str, Any] = {
            "stages": {}
        }

        # Analysis is the root
        # dependency for the rest
        # of the software workflow.
        analysis_result = self._execute_stage(
            "analysis",
            context=context
        )

        workflow_data["stages"]["analysis"] = (
            analysis_result.to_dict()
        )

        if not analysis_result.success:
            return analysis_result

        architecture = self._result_value(
            analysis_result,
            "architecture"
        )

        if architecture is None:
            return self._workflow_failure(
                "analysis",
                "Analysis completed without architecture output.",
                workflow_data
            )

        workflow_data["architecture"] = architecture

        # Documentation must use
        # MemoryAgent through the
        # DocumentationPipeline and
        # must receive the analyzed
        # architecture.
        if self._is_single_file_architecture(architecture):
            documentation_result = None
            memory_docs = {
                "memory_files": {},
            }
        else:
            documentation_result = self._execute_stage(
                "documentation",
                context=context,
                architecture=architecture
            )

            workflow_data["stages"]["documentation"] = (
                documentation_result.to_dict()
            )

            if not documentation_result.success:
                return documentation_result

            memory_docs = self._result_value(
                documentation_result,
                "documentation"
            )

        # Generation consumes both
        # context and architecture.
        generation_result = self._execute_stage(
            "generation",
            context=context,
            architecture=architecture,
            memory_docs=memory_docs
        )

        workflow_data["stages"]["generation"] = (
            generation_result.to_dict()
        )

        if not generation_result.success:
            return generation_result

        implementation = self._result_value(
            generation_result,
            "implementation"
        )

        if implementation is None:
            return self._workflow_failure(
                "generation",
                "Generation completed without implementation output.",
                workflow_data
            )

        workflow_data["implementation"] = implementation

        # Validation failures are
        # repairable.  The failed
        # validation result is kept
        # in workflow_data before
        # repair mutates the current
        # implementation reference.
        validation_result = self._execute_validation(
            context=context,
            architecture=architecture,
            implementation=implementation
        )

        workflow_data["stages"]["validation"] = (
            validation_result.to_dict()
        )

        repair_result = None

        if not validation_result.success:
            repair_result = self._execute_repair(
                context=context,
                implementation=implementation,
                failed_result=validation_result,
                retry_count=0
            )

            workflow_data["stages"]["validation_repair"] = (
                repair_result.to_dict()
            )

            if not repair_result.success:
                return repair_result

            implementation = self._updated_implementation(
                current=implementation,
                repair_result=repair_result
            )

            workflow_data["implementation"] = implementation

        sandbox_result = self._execute_sandbox(
            context=context,
            architecture=architecture,
            implementation=implementation
        )

        workflow_data["stages"]["sandbox"] = (
            sandbox_result.to_dict()
        )

        healing_result = self._execute_healing(
            context=context,
            architecture=architecture,
            implementation=implementation,
            validation_result=validation_result,
            sandbox_result=sandbox_result,
            repair_result=repair_result
        )

        workflow_data["stages"]["healing"] = (
            healing_result.to_dict()
        )

        if not healing_result.success:
            return healing_result

        implementation = self._updated_implementation(
            current=implementation,
            repair_result=healing_result
        )

        workflow_data["implementation"] = implementation

        review_result = self._execute_stage(
            "review",
            context=context,
            implementation=implementation
        )

        workflow_data["stages"]["review"] = (
            review_result.to_dict()
        )

        if not review_result.success:
            return review_result

        review = self._result_value(
            review_result,
            "review"
        )

        if review is None:
            return self._workflow_failure(
                "review",
                "Review completed without review output.",
                workflow_data
            )

        testing_result = self._execute_stage(
            "testing",
            context=context,
            review=review
        )

        workflow_data["stages"]["testing"] = (
            testing_result.to_dict()
        )

        if not testing_result.success:
            return testing_result

        return PipelineResult.success_result(
            pipeline="generation",
            data=workflow_data
        )

    # ------------------------------------------------------------------
    # Stage Execution Helpers
    # ------------------------------------------------------------------

    def _execute_stage(
        self,
        name: str,
        **kwargs: Any
    ) -> PipelineResult:
        """
        Execute one registered
        PipelineResult-based stage.

        Why:

        Most first-party pipelines
        already return PipelineResult.
        This helper adds consistent
        exception normalization for
        workflow orchestration without
        changing direct pipeline
        execution semantics.
        """

        try:
            pipeline = self.get_pipeline(
                name
            )

            result = pipeline.execute(
                **kwargs
            )

        except Exception as error:
            self.logger.error(
                f"{name.title()} stage failed: {error}"
            )

            return PipelineResult.failure_result(
                pipeline=name,
                data={
                    "error":
                        str(error)
                }
            )

        return self._normalize_result(
            name,
            result
        )

    def _execute_validation(
        self,
        *,
        context,
        architecture: ArchitectureBlueprint,
        implementation: dict[str, Any]
    ) -> PipelineResult:
        """
        Run ValidationPipeline
        and convert its dictionary
        contract into PipelineResult.
        """

        try:
            validation = self.get_pipeline(
                "validation"
            )

            result = validation.execute(
                project_path=context.generated_project,
                architecture=architecture,
                implementation=implementation
            )

        except Exception as error:
            self.logger.error(
                f"Validation stage failed: {error}"
            )

            return PipelineResult.failure_result(
                pipeline="validation",
                data={
                    "error":
                        str(error)
                }
            )

        return self._normalize_result(
            "validation",
            result,
            success_key="passed"
        )

    def _execute_project(
        self,
        *,
        context,
        architecture: ArchitectureBlueprint,
        **kwargs: Any
    ) -> PipelineResult:
        """
        Run ExecutionPipeline
        against the generated
        project.

        Callers may inject:

        - runner
        - execution_command
        - working_directory

        The architecture may also
        define run_command,
        execution_command or command
        inside architecture_spec.
        """

        runner = kwargs.get(
            "runner"
        )

        command = self._resolve_execution_command(
            architecture=architecture,
            kwargs=kwargs
        )

        working_directory = (
            kwargs.get(
                "working_directory"
            )
            or context.generated_project
        )

        if runner is None:
            return self._workflow_failure(
                "execution",
                "Execution runner is required for ExecutionPipeline."
            )

        if command is None:
            return self._workflow_failure(
                "execution",
                "Execution command is required for ExecutionPipeline."
            )

        try:
            execution = self.get_pipeline(
                "execution"
            )

            result = execution.execute(
                runner=runner,
                command=command,
                working_directory=working_directory
            )

        except Exception as error:
            self.logger.error(
                f"Execution stage failed: {error}"
            )

            return PipelineResult.failure_result(
                pipeline="execution",
                data={
                    "error":
                        str(error)
                }
            )

        return self._normalize_result(
            "execution",
            result,
            success_key="healthy"
        )

    def _execute_sandbox(
        self,
        *,
        context,
        architecture: ArchitectureBlueprint,
        implementation: dict[str, Any]
    ) -> PipelineResult:
        try:
            sandbox = self.get_pipeline(
                "sandbox"
            )

            result = sandbox.execute(
                context=context,
                architecture=architecture,
                implementation=implementation
            )

        except Exception as error:
            self.logger.error(
                f"Sandbox stage failed: {error}"
            )

            return PipelineResult.failure_result(
                pipeline="sandbox",
                data={
                    "error":
                        str(error)
                }
            )

        return self._normalize_result(
            "sandbox",
            result
        )

    def _execute_healing(
        self,
        *,
        context,
        architecture: ArchitectureBlueprint,
        implementation: dict[str, Any],
        validation_result: PipelineResult,
        sandbox_result: PipelineResult,
        repair_result: PipelineResult | None
    ) -> PipelineResult:
        try:
            healing = self.get_pipeline(
                "healing"
            )

            result = healing.execute(
                context=context,
                architecture=architecture,
                implementation=implementation,
                validation_result=validation_result,
                sandbox_result=sandbox_result,
                repair_result=repair_result
            )

        except Exception as error:
            self.logger.error(
                f"Healing stage failed: {error}"
            )

            return PipelineResult.failure_result(
                pipeline="healing",
                data={
                    "error":
                        str(error)
                }
            )

        return self._normalize_result(
            "healing",
            result
        )

    def _execute_repair(
        self,
        *,
        context,
        implementation: dict[str, Any],
        failed_result: PipelineResult,
        retry_count: int
    ) -> PipelineResult:
        """
        Execute RepairPipeline for
        validation or execution
        failures only.

        Why:

        Repair is a recovery concern,
        not a normal stage. Keeping it
        here prevents repair behavior
        from leaking into mandatory
        pipeline orchestration.
        """

        return self._execute_stage(
            "repair",
            context=context,
            implementation=implementation,
            error=self._failure_message(
                failed_result
            ),
            retry_count=retry_count
        )

    # ------------------------------------------------------------------
    # Result Helpers
    # ------------------------------------------------------------------

    def _normalize_result(
        self,
        pipeline: str,
        result: Any,
        success_key: str | None = None
    ) -> PipelineResult:
        """
        Convert supported stage
        outputs into PipelineResult.
        """

        if isinstance(
            result,
            PipelineResult
        ):
            return result

        if isinstance(
            result,
            dict
        ):
            if success_key is None:
                success = True
            else:
                success = bool(
                    result.get(
                        success_key
                    )
                )

            if success:
                return PipelineResult.success_result(
                    pipeline=pipeline,
                    data=result
                )

            return PipelineResult.failure_result(
                pipeline=pipeline,
                data=result
            )

        return PipelineResult.failure_result(
            pipeline=pipeline,
            data={
                "error":
                    (
                        "Pipeline returned unsupported "
                        f"result type: {type(result).__name__}"
                    )
            }
        )

    def _result_value(
        self,
        result: PipelineResult,
        key: str
    ) -> Any:
        """
        Read a value from a
        PipelineResult data payload.
        """

        return result.data.get(
            key
        )

    def _updated_implementation(
        self,
        *,
        current: dict[str, Any],
        repair_result: PipelineResult
    ) -> dict[str, Any]:
        """
        Return repaired
        implementation when
        RepairPipeline produced one.
        """

        repaired = repair_result.data.get(
            "implementation"
        )

        if isinstance(
            repaired,
            dict
        ):
            return repaired

        return current

    def _failure_message(
        self,
        result: PipelineResult
    ) -> str:
        """
        Build a compact failure
        message for RepairPipeline.
        """

        error = result.data.get(
            "error"
        )

        if error:
            return str(
                error
            )

        messages = []
        report = result.data.get(
            "report",
            {}
        )

        if isinstance(
            report,
            dict
        ):
            for section in report.values():
                if not isinstance(
                    section,
                    dict
                ):
                    continue

                messages.extend(
                    str(item)
                    for item in section.get(
                        "errors",
                        []
                    )
                )

        logs = result.data.get(
            "logs",
            {}
        )

        if isinstance(
            logs,
            dict
        ):
            stderr = logs.get(
                "stderr"
            )

            if stderr:
                messages.append(
                    str(stderr)
                )

        if messages:
            return "\n".join(
                messages
            )

        return str(
            result.to_dict()
        )

    def _workflow_failure(
        self,
        pipeline: str,
        message: str,
        data: dict[str, Any] | None = None
    ) -> PipelineResult:
        """
        Create a standardized
        workflow failure result.
        """

        payload = dict(
            data or {}
        )

        payload["error"] = message

        return PipelineResult.failure_result(
            pipeline=pipeline,
            data=payload
        )

    def _resolve_execution_command(
        self,
        *,
        architecture: ArchitectureBlueprint,
        kwargs: dict[str, Any]
    ) -> list[str] | None:
        """
        Resolve the command for
        ExecutionPipeline.

        Preference order:

        1. execute(...,
           execution_command=[...])
        2. execute(...,
           command=[...])
        3. architecture_spec
           command metadata.
        """

        command = (
            kwargs.get(
                "execution_command"
            )
            or kwargs.get(
                "command"
            )
        )

        if command is None:
            architecture_spec = architecture.metadata.get(
            "architecture_spec",
            {}
        )

            command = (
                architecture_spec.get(
                    "execution_command"
                )
                or architecture_spec.get(
                    "run_command"
                )
                or architecture_spec.get(
                    "command"
                )
            )

        if command is None:
            return None

        if isinstance(
            command,
            list
        ):
            return [
                str(part)
                for part in command
            ]

        if isinstance(
            command,
            str
        ):
            return command.split()

        return None

    # ----------------------------------
    # List Pipelines
    # ----------------------------------

    def list_pipelines(
        self
    ) -> list[str]:
        """
        Return all
        registered
        pipelines.

        Why:

        Useful for
        debugging,
        diagnostics,
        testing and
        CLI commands.
        """

        # Return the names
        # of every registered
        # pipeline.
        return sorted(

            self._pipelines.keys()

        )

    def _is_single_file_architecture(
        self,
        architecture,
    ) -> bool:
        if hasattr(
            architecture,
            "get",
        ):
            framework_template = architecture.get(
                "framework_template",
                "",
            )
        else:
            framework_template = getattr(
                architecture,
                "framework_template",
                "",
            )

        return str(
            framework_template
        ).lower() == "single_file_python"

    # ----------------------------------
    # Pipeline Count
    # ----------------------------------

    def pipeline_count(
        self
    ) -> int:
        """
        Return the total
        number of registered
        pipelines.

        Why:

        Useful for startup
        verification and
        diagnostics to ensure
        all expected pipelines
        were registered.
        """

        # Return the total
        # number of registered
        # pipelines.
        return len(
            self._pipelines
        )

    # ----------------------------------
    # Clear Pipelines
    # ----------------------------------

    def clear(
        self
    ) -> None:
        """
        Remove all
        registered pipelines.

        Why:

        Useful during
        testing or when
        reconfiguring the
        PipelineExecutor.

        This ensures the
        executor starts
        with a clean state.
        """

        # Remove every
        # registered pipeline.
        self._pipelines.clear()

        # Reset pipeline
        # instance references.
        self.analysis_pipeline = None

        self.generation_pipeline = None

        self.repair_pipeline = None

        self.review_pipeline = None

        self.testing_pipeline = None
        self.sandbox_pipeline = None
        self.healing_pipeline = None

        self.documentation_pipeline = None

        self.validation_pipeline = None

        self.execution_pipeline = None

        self.logger.info(
            "Pipeline registry cleared."
        )

"""
File:
core/pipeline/documentation_pipeline.py

Purpose:
Execute the
documentation
pipeline.

Why:

Separates documentation
generation from code
generation and analysis.

Allows KAIROS to
generate project
documentation without
coupling documentation
logic to the CLI manager.

Responsibilities:

- Generate all project
  documentation through
  MemoryAgent.
- Use PipelineContext as
  the source of project
  orchestration state.
- Return a standard
  PipelineResult.

Does NOT:

- Generate source code.
- Validate code.
- Execute code.
- Repair code.
- Depend on CLIManager.

Architecture:

CLI Manager
      |
      v
Pipeline Executor
      |
      v
Documentation Pipeline
      |
      +-- MemoryAgent
      |
      v
Pipeline Result
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.logging.kairos_logger import (
    KairosLogger
)

from core.pipeline.pipeline_context import (
    PipelineContext
)

from core.pipeline.pipeline_result import (
    PipelineResult
)


class DocumentationPipeline:
    """
    Execute the
    documentation
    workflow.
    """

    def __init__(
        self,
        memory_agent
    ) -> None:
        """
        Purpose:
        Initialize the
        documentation pipeline.

        Why:
        KAIROS V1 uses
        MemoryAgent as the
        documentation source
        for project memory,
        architecture notes,
        roadmap and context.

        Returns:
        None.

        Raises:
        None.
        """

        self.logger = (
            KairosLogger(
                "documentation_pipeline"
            )
        )

        # MemoryAgent owns the
        # V1 documentation API.
        self.memory_agent = (
            memory_agent
        )

    # ----------------------------------
    # Execute Pipeline
    # ----------------------------------

    def execute(
        self,
        context: PipelineContext,
        architecture: dict[str, Any]
    ) -> PipelineResult:
        """
        Purpose:
        Execute the
        documentation pipeline.

        Why:
        Documentation generation
        must be delegated to
        MemoryAgent so the CLI
        remains an orchestrator
        and the pipeline remains
        independent from CLIManager.

        Returns:
        PipelineResult containing
        generated documentation
        and documentation context.

        Raises:
        Propagates MemoryAgent
        failures when documentation
        generation cannot complete.
        """

        self.logger.info(
            "Documentation Started"
        )

        project_name = (
            self._project_name(
                context,
                architecture
            )
        )

        documentation_input = (
            self._build_documentation_input(
                context=context,
                architecture=architecture,
                project_name=project_name
            )
        )

        # MemoryAgent.generate_all is
        # the V1 API for producing the
        # complete KAIROS documentation
        # package for a project.
        documentation = (
            self.memory_agent.generate_all(
                documentation_input
            )
        )

        self.logger.success(
            "Documentation completed"
        )

        # Return a standardized
        # pipeline result so the
        # Pipeline Executor can
        # process every pipeline
        # identically.
        return PipelineResult.success_result(

            pipeline="documentation",

            data={

                "project_name":
                    project_name,

                "generated_project":
                    context.generated_project,

                "shared_context":
                    context.shared_context,

                "architecture":
                    architecture,

                # Complete project
                # documentation generated
                # by MemoryAgent.
                "documentation":
                    documentation,

            }

        )

    # ----------------------------------
    # Documentation Input
    # ----------------------------------

    def _build_documentation_input(
        self,
        *,
        context: PipelineContext,
        architecture: dict[str, Any],
        project_name: str
    ) -> dict[str, Any]:
        """
        Purpose:
        Build the architecture
        payload sent to MemoryAgent.

        Why:
        MemoryAgent accepts the
        architecture object as its
        documentation source.  This
        method enriches that object
        with PipelineContext details
        without coupling MemoryAgent
        to pipeline internals.

        Returns:
        A dictionary containing
        architecture plus project,
        workspace and context
        metadata.

        Raises:
        None.
        """

        return {

            "project_name":
                project_name,

            "generated_project":
                context.generated_project,

            "target_project":
                context.target_project,

            "shared_context":
                context.shared_context,

            "architecture":
                architecture,

        }

    # ----------------------------------
    # Project Name
    # ----------------------------------

    def _project_name(
        self,
        context: PipelineContext,
        architecture: dict[str, Any]
    ) -> str:
        """
        Purpose:
        Resolve the project
        name for documentation.

        Why:
        Project names may come
        from architecture output,
        context metadata, the
        generated workspace or
        the target project path.

        Returns:
        A non-empty project name.

        Raises:
        None.
        """

        architecture_spec = (
            architecture.get(
                "architecture_spec",
                {}
            )
        )

        metadata = (
            context.shared_context.get(
                "metadata",
                {}
            )
        )

        return (
            architecture_spec.get(
                "project_name"
            )
            or architecture.get(
                "project_name"
            )
            or metadata.get(
                "project_name"
            )
            or Path(
                context.generated_project
            ).name
            or Path(
                context.target_project
            ).name
            or "KAIROS"
        )

    # ----------------------------------
    # Pipeline Name
    # ----------------------------------

    @property
    def name(
        self
    ) -> str:
        """
        Purpose:
        Return the
        pipeline name.

        Why:
        PipelineExecutor registers
        and executes pipelines by
        stable names.

        Returns:
        The documentation pipeline
        name.

        Raises:
        None.
        """

        return "documentation"

    # ----------------------------------
    # Supports Pipeline
    # ----------------------------------

    def supports(
        self,
        pipeline: str
    ) -> bool:
        """
        Purpose:
        Check whether this
        pipeline can execute
        the requested task.

        Why:
        Capability checks allow
        future registries to verify
        pipeline compatibility.

        Returns:
        True when pipeline matches
        this pipeline name.

        Raises:
        None.
        """

        return (
            pipeline ==
            self.name
        )

"""
File:
core/pipeline/testing_pipeline.py

Purpose:
Execute the
testing pipeline.

Why:

Separates project
testing from review,
generation and repair.

Allows KAIROS to
verify generated or
repaired projects
without coupling
testing logic to
the CLI manager.

Responsibilities:

- Execute tests.
- Collect test results.
- Return a standard
  pipeline result.

Does NOT:

- Generate code.
- Repair code.
- Validate code.
- Execute application.

Architecture:

CLI Manager
      │
      ▼
Pipeline Executor
      │
      ▼
Testing Pipeline
      │
      ├── Tester Agent
      └── Pipeline Result
"""

from __future__ import annotations

from core.logging.kairos_logger import (
    KairosLogger
)

from core.pipeline.pipeline_context import (
    PipelineContext
)

from core.pipeline.pipeline_result import (
    PipelineResult
)


class TestingPipeline:
    """
    Execute the
    testing workflow.
    """

    def __init__(
        self,
        tester
    ):
        """
        Initialize the
        testing pipeline.
        """

        self.logger = (
            KairosLogger(
                "testing_pipeline"
            )
        )

        # AI agent responsible
        # for executing tests
        # on the generated
        # or repaired project.
        self.tester = (
            tester
        )
        
    
    # ----------------------------------
    # Execute Pipeline
    # ----------------------------------

    def execute(
        self,
        context: PipelineContext,
        review: dict|None = None
    ) -> PipelineResult:
        """
        Execute the
        testing pipeline.
        """

        self.logger.info(
            "Testing Started"
        )

        # Ask the Tester
        # Agent to execute
        # project tests.
        
        if review is None:
            review = {}
    
        testing = (
            self.tester.run_tests(

                review,

                context=context.shared_context

            )
        )

        self.logger.success(
            "Testing completed"
        )
        
        # Return a standardized
        # pipeline result so the
        # Pipeline Executor can
        # process every pipeline
        # identically.
        return PipelineResult.success_result(

            pipeline="testing",

            data={

                # Complete testing
                # report generated
                # by the Tester Agent.
                "testing":
                    testing,

            }

        )
    
    # ----------------------------------
    # Pipeline Name
    # ----------------------------------

    @property  # Read-only property. Access like obj.name instead of obj.name().
    def name(
        self
    ) -> str:
        """
        Return the
        pipeline name.
        """

        return "testing"
    
    
    # ----------------------------------
    # Supports Pipeline
    # ----------------------------------

    def supports(
        self,
        pipeline: str
    ) -> bool:
        """
        Check whether this
        pipeline can execute
        the requested task.
        """

        return (
            pipeline ==
            self.name
        )
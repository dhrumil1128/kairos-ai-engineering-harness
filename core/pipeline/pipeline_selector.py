"""
File:
core/pipeline/pipeline_selector.py

Purpose:
Select the correct
execution pipeline
based on the user's
intent.

Architecture:

User Prompt
      │
      ▼
Pipeline Selector
      │
      ├── Analysis
      ├── Generation
      ├── Repair
      ├── Review
      ├── Testing
      └── Documentation
"""

from __future__ import annotations

from core.logging.kairos_logger import (
    KairosLogger
)

from core.pipeline.pipeline_registry import (
    PipelineRegistry
)


class PipelineSelector:
    """
    Decide which pipeline
    should execute.
    """

    def __init__(
        self
    ):
        """
        Initialize selector.
        """

        self.logger = (
            KairosLogger(
                "pipeline"
            )
        )
        
        self.registry = (
            PipelineRegistry()
        )
    
   

    # ----------------------------------
    # Select Pipeline
    # ----------------------------------

    def select(
        self,
        command: str
    ) -> str:
        """
        Select the
        execution pipeline.
        """

        pipeline = (
            self.registry.find_pipeline(
                command
            )
        )

        if pipeline:

            self.logger.info(
                f"Pipeline: {pipeline.title()}"
            )

            return pipeline

        self.logger.info(
            "Pipeline: Generation"
        )

        return "generation"
"""
File:
core/pipeline/pipeline_context.py

Purpose:
Shared execution
context for every
pipeline.

Architecture:

CLI Manager
      │
      ▼
Pipeline Context
      │
      ▼
Pipeline Executor
      │
      ▼
Analysis / Generation /
Repair / Review /
Testing / Documentation
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class PipelineContext:
    """
    Shared context passed
    to every pipeline.
    """

    command: str

    target_project: str

    generated_project: str

    shared_context: dict[str, Any]
    

  
    
    # ----------------------------------
    # Context Helpers
    # ----------------------------------

    @property
    def is_analysis(
        self
    ) -> bool:
        """
        Read-only project.
        """

        return (
            self.target_project
            != ""
        )

    @property
    def is_generation(
        self
    ) -> bool:
        """
        Generate project.
        """

        return (
            self.generated_project
            != ""
        )
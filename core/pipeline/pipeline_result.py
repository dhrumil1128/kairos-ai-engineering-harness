"""
File:
core/pipeline/pipeline_result.py

Purpose:
Standard result object
returned by every
pipeline.

Architecture:

Pipeline
     │
     ▼
Pipeline Result
     │
     ▼
CLI Manager
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class PipelineResult:
    """
    Standard pipeline
    execution result.
    """

    status: str

    pipeline: str

    success: bool

    data: dict[str, Any]
    
    
    # ----------------------------------
    # Success Result
    # ----------------------------------

    @classmethod   # Creates a PipelineResult object without creating an instance first.
    def success_result(
        cls,   # cls refers to the PipelineResult class itself.
        pipeline: str,
        data: dict[str, Any]
    ) -> "PipelineResult":
        """
        Create a successful
        pipeline result.
        """

        return cls(

            status="completed",

            pipeline=pipeline,

            success=True,

            data=data

        )

    # ----------------------------------
    # Failure Result
    # ----------------------------------

    @classmethod        # Creates a failed PipelineResult object.
    def failure_result(
        cls,        # cls refers to the PipelineResult class.
        pipeline: str,
        data: dict[str, Any]
    ) -> "PipelineResult":
        """
        Create a failed
        pipeline result.
        """

        return cls(

            status="failed",

            pipeline=pipeline,

            success=False,

            data=data

        )
        
    # ----------------------------------
    # Convert To Dictionary
    # ----------------------------------

    def to_dict(
        self
    ) -> dict[str, Any]:
        """
        Convert the result
        into a dictionary.
        """

        return {

            "status":
                self.status,

            "pipeline":
                self.pipeline,

            "success":
                self.success,

            "data":
                self.data,

        }
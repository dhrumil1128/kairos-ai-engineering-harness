"""
File: core/context/context_pipeline.py

Purpose:
Coordinate the complete
Context Intelligence
workflow.

Why:

This pipeline connects all
Context Engine components
into a single workflow
before every LLM request.

Architecture:

Project Loader
        │
        ▼
Document Parser
        │
        ▼
Knowledge Manager
        │
        ▼
Project Context
        │
        ▼
Context Loader
        │
        ▼
Context Ranker
        │
        ▼
Prompt Builder

V2:
- Semantic Pipeline

V3:
- Adaptive Pipeline

V4:
- Multi-Agent Context

V5:
- Autonomous Context
"""

from __future__ import annotations

from core.logging.kairos_logger import (
    KairosLogger,
)

from core.context.project_context import (
    ProjectContext
)

from core.context.context_loader import (
    ContextLoader
)

from core.context.context_ranker import (
    ContextRanker
)


class ContextPipeline:
    """
    Enterprise Context
    Pipeline.
    """

    def __init__(
        self
    ):
        """
        Initialize
        pipeline.
        """

        self.logger = (
            KairosLogger(
                "context"
            )
        )

        self.project_context = (
            ProjectContext()
        )

        self.loader = (
            ContextLoader()
        )

        self.ranker = (
            ContextRanker()
        )

    # ---------------------------------- #
    # Add Document
    # ---------------------------------- #

    def add_document(
        self,
        name: str,
        content
    ) -> None:
        """
        Add parsed
        document.
        """

        self.project_context.add_document(
            name,
            content
        )

    # ---------------------------------- #
    # Build Context
    # ---------------------------------- #

    def build_context(
        self
    ) -> dict:
        """
        Build complete
        context.
        """

        self.logger.info(
            "Building Context Pipeline."
        )

        return (
            self.loader.build_context(
                self.project_context
            )
        )
        
    
    # ---------------------------------- #
    # Rank Context
    # ---------------------------------- #

    def rank_context(
        self,
        query: str,
        top_k: int = 10
    ) -> list[str]:
        """
        Rank project
        context.
        """

        context = (
            self.build_context()
        )

        documents = []

        for document in (

            context[
                "documents"
            ].values()

        ):

            documents.append(
                str(document)
            )

        ranked = (
            self.ranker.top_k(
                documents,
                query,
                top_k
            )
        )

        self.logger.success(
            "Context ranked."
        )

        return ranked

    # ---------------------------------- #
    # Export Context
    # ---------------------------------- #

    def export(
        self
    ) -> dict:
        """
        Export complete
        pipeline context.
        """

        return (
            self.build_context()
        )

    # ---------------------------------- #
    # Context Summary
    # ---------------------------------- #

    def summary(
        self
    ) -> dict:
        """
        Return pipeline
        summary.
        """

        context = (
            self.build_context()
        )

        return self.loader.summary(
            context
        )
        
        
    # ---------------------------------- #
    # Validation
    # ---------------------------------- #

    def document_count(
        self
    ) -> int:
        """
        Return total
        loaded documents.
        """

        return (
            self.project_context
            .document_count()
        )

    # ---------------------------------- #
    # Reset Pipeline
    # ---------------------------------- #

    def clear(
        self
    ) -> None:
        """
        Reset Context
        Pipeline.
        """

        self.project_context.clear()

        self.logger.info(
            "Context Pipeline reset."
        )
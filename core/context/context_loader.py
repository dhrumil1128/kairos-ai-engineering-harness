"""
File: core/context/context_loader.py

Purpose:
Load only the required
project context before
LLM execution.

Why:

Instead of sending every
project document, KAIROS
loads only the context
required for the current
task.

Architecture:

Project Context
        │
        ▼
Context Loader
        │
        ├── Load Documents
        ├── Load Metadata
        ├── Load Knowledge
        ├── Load Session
        │
        ▼
Context Ranker

V2:
- Semantic Retrieval

V3:
- Dependency Loading

V4:
- Dynamic Context

V5:
- Predictive Context
"""

from __future__ import annotations

from pathlib import Path

from core.logging.kairos_logger import (
    KairosLogger,
)


class ContextLoader:
    """
    Enterprise Context
    Loader.
    """

    def __init__(
        self
    ):
        """
        Initialize loader.
        """

        self.logger = (
            KairosLogger(
                "context"
            )
        )

    # ---------------------------------- #
    # Load File
    # ---------------------------------- #

    def load_file(
        self,
        file_path: str
    ) -> str:
        """
        Load context file.
        """

        path = Path(
            file_path
        )

        if (
            not path.exists()
        ):

            self.logger.warning(
                f"Missing: {file_path}"
            )

            return ""

        self.logger.info(
            f"Loading: {path.name}"
        )

        return path.read_text(
            encoding="utf-8"
        )

    # ---------------------------------- #
    # Load Documents
    # ---------------------------------- #

    def load_documents(
        self,
        project_context
    ) -> dict:
        """
        Load parsed
        documents.
        """

        self.logger.info(
            "Loading documents."
        )

        return (
            project_context
            .all_documents()
        )

    # ---------------------------------- #
    # Load Metadata
    # ---------------------------------- #

    def load_metadata(
        self,
        project_context
    ) -> dict:
        """
        Load project
        metadata.
        """

        self.logger.info(
            "Loading metadata."
        )

        return (
            project_context
            .metadata
        )
        
        # ---------------------------------- #
    # Load Knowledge
    # ---------------------------------- #

    def load_knowledge(
        self,
        project_context
    ) -> dict:
        """
        Load Knowledge
        Index.
        """

        self.logger.info(
            "Loading Knowledge Index."
        )

        return (
            project_context
            .get_knowledge()
        )

    # ---------------------------------- #
    # Load Session
    # ---------------------------------- #

    def load_session(
        self,
        project_context
    ) -> dict:
        """
        Load session
        context.
        """

        self.logger.info(
            "Loading session."
        )

        return (
            project_context
            .get_session()
        )

    # ---------------------------------- #
    # Build Context
    # ---------------------------------- #

    def build_context(
        self,
        project_context
    ) -> dict:
        """
        Build complete
        context object.
        """

        self.logger.info(
            "Building context."
        )

        context = {

            "documents":
            self.load_documents(
                project_context
            ),

            "metadata":
            self.load_metadata(
                project_context
            ),

            "knowledge":
            self.load_knowledge(
                project_context
            ),

            "session":
            self.load_session(
                project_context
            ),

        }

        self.logger.success(
            "Context built."
        )

        return context
    
    
        # ---------------------------------- #
    # Validation
    # ---------------------------------- #

    def file_exists(
        self,
        file_path: str
    ) -> bool:
        """
        Check whether
        file exists.
        """

        return Path(
            file_path
        ).exists()

    # ---------------------------------- #
    # Context Summary
    # ---------------------------------- #

    def summary(
        self,
        context: dict
    ) -> dict:
        """
        Return context
        summary.
        """

        return {

            "documents":
            len(
                context.get(
                    "documents",
                    {}
                )
            ),

            "metadata":
            len(
                context.get(
                    "metadata",
                    {}
                )
            ),

            "knowledge":
            len(
                context.get(
                    "knowledge",
                    {}
                )
            ),

            "session":
            len(
                context.get(
                    "session",
                    {}
                )
            ),

        }

    # ---------------------------------- #
    # Clear Context
    # ---------------------------------- #

    def clear(
        self
    ) -> None:
        """
        Clear loader
        state.
        """

        self.logger.info(
            "Context Loader reset."
        )
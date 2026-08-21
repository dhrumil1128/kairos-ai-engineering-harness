"""
File: core/context/project_context.py

Purpose:
Build the unified
Context Object shared
by every KAIROS agent.

Why:

Instead of every agent
loading project files,
they all consume a
single Context Object.

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
      ├── Documents
      ├── Metadata
      ├── Knowledge
      ├── Session
      │
      ▼
Planner
Architect
Coder
Reviewer
Tester
Healing

V2:
- Context Snapshots

V3:
- Shared Agent Memory

V4:
- Distributed Context

V5:
- Persistent Context Cache
"""

from __future__ import annotations

from core.logging.kairos_logger import (
    KairosLogger,
)


class ProjectContext:
    """
    Unified Context Object.
    """

    def __init__(
        self
    ):
        """
        Initialize context.
        """

        self.logger = (
            KairosLogger(
                "context"
            )
        )

        self.documents = {}

        self.metadata = {}

        self.knowledge = {}

        self.session = {}

    # ---------------------------------- #
    # Documents
    # ---------------------------------- #

    def add_document(
        self,
        name: str,
        content
    ) -> None:
        """
        Store parsed
        document.
        """

        self.documents[
            name
        ] = content

        self.logger.info(
            f"Document: {name}"
        )

    def document(
        self,
        name: str
    ):
        """
        Return document.
        """

        return self.documents.get(
            name
        )

    # ---------------------------------- #
    # Metadata
    # ---------------------------------- #

    def set_metadata(
        self,
        metadata: dict
    ) -> None:
        """
        Store project
        metadata.
        """

        self.metadata = metadata

        self.logger.info(
            "Metadata updated."
        )
        
        
        # ---------------------------------- #
    # Knowledge
    # ---------------------------------- #

    def set_knowledge(
        self,
        knowledge: dict
    ) -> None:
        """
        Store Knowledge
        Index.
        """

        self.knowledge = (
            knowledge
        )

        self.logger.info(
            "Knowledge updated."
        )

    def get_knowledge(
        self
    ) -> dict:
        """
        Return Knowledge
        Index.
        """

        return (
            self.knowledge
        )

    # ---------------------------------- #
    # Session Context
    # ---------------------------------- #

    def set_session(
        self,
        session: dict
    ) -> None:
        """
        Store current
        session context.
        """

        self.session = (
            session
        )

        self.logger.info(
            "Session updated."
        )

    def get_session(
        self
    ) -> dict:
        """
        Return current
        session.
        """

        return (
            self.session
        )

    # ---------------------------------- #
    # Context Summary
    # ---------------------------------- #

    def summary(
        self
    ) -> dict:
        """
        Return Context
        summary.
        """

        return {

            "documents":
            len(
                self.documents
            ),

            "metadata":
            len(
                self.metadata
            ),

            "knowledge":
            len(
                self.knowledge
            ),

            "session":
            len(
                self.session
            ),

        }

    # ---------------------------------- #
    # Documents
    # ---------------------------------- #

    def all_documents(
        self
    ) -> dict:
        """
        Return all
        documents.
        """

        return (
            self.documents
        )
        
        
        # ---------------------------------- #
    # Validation
    # ---------------------------------- #

    def document_exists(
        self,
        name: str
    ) -> bool:
        """
        Check whether
        document exists.
        """

        return (
            name
            in self.documents
        )

    def document_count(
        self
    ) -> int:
        """
        Return total
        documents.
        """

        return len(
            self.documents
        )

    # ---------------------------------- #
    # Clear Context
    # ---------------------------------- #

    def clear(
        self
    ) -> None:
        """
        Clear complete
        project context.
        """

        self.logger.warning(
            "Clearing Project Context."
        )

        self.documents.clear()

        self.metadata.clear()

        self.knowledge.clear()

        self.session.clear()

    # ---------------------------------- #
    # Export Context
    # ---------------------------------- #

    def export(
        self
    ) -> dict:
        """
        Export complete
        context object.
        """

        return {

            "documents":
            self.documents,

            "metadata":
            self.metadata,

            "knowledge":
            self.knowledge,

            "session":
            self.session,

        }
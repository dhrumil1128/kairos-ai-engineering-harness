"""
File: core/context/knowledge_manager.py

Purpose:
Build and manage the
Knowledge Index used by
the KAIROS Context
Intelligence Engine.

Why:

Every agent should use
the same project knowledge
instead of repeatedly
reading project files.

Architecture:

Project Loader
      │
      ▼
Document Parser
      │
      ▼
Knowledge Manager
      │
      ├── Knowledge Index
      ├── Dependency Map
      ├── Architecture Map
      ├── Module Registry
      │
      ▼
All Agents

V2:
- Semantic Retrieval

V3:
- Vector Index

V4:
- Knowledge Graph

V5:
- Distributed Memory
"""

from __future__ import annotations

from core.logging.kairos_logger import (
    KairosLogger,
)


class KnowledgeManager:
    """
    Enterprise Knowledge
    Manager.
    """

    def __init__(
        self
    ):
        """
        Initialize storage.
        """

        self.logger = (
            KairosLogger(
                "context"
            )
        )

        self.knowledge = {}

        self.modules = {}

        self.dependencies = {}

        self.architecture = {}

    # ---------------------------------- #
    # Store Knowledge
    # ---------------------------------- #

    def store(
        self,
        key: str,
        value
    ) -> None:
        """
        Store knowledge.
        """

        self.logger.info(
            f"Storing: {key}"
        )

        self.knowledge[
            key
        ] = value

    # ---------------------------------- #
    # Retrieve Knowledge
    # ---------------------------------- #

    def retrieve(
        self,
        key: str
    ):
        """
        Retrieve knowledge.
        """

        return self.knowledge.get(
            key
        )

    # ---------------------------------- #
    # Register Module
    # ---------------------------------- #

    def register_module(
        self,
        module: str,
        metadata: dict
    ) -> None:
        """
        Register project
        module.
        """

        self.modules[
            module
        ] = metadata

        self.logger.info(
            f"Module: {module}"
        )

    # ---------------------------------- #
    # Register Dependency
    # ---------------------------------- #

    def register_dependency(
        self,
        file_name: str,
        dependencies: list[str]
    ) -> None:
        """
        Register file
        dependencies.
        """

        self.dependencies[
            file_name
        ] = dependencies
        
        
        # ---------------------------------- #
    # Register Architecture
    # ---------------------------------- #

    def register_architecture(
        self,
        component: str,
        metadata: dict
    ) -> None:
        """
        Register architecture
        component.
        """

        self.architecture[
            component
        ] = metadata

        self.logger.info(
            f"Architecture: {component}"
        )

    # ---------------------------------- #
    # Module Information
    # ---------------------------------- #

    def module(
        self,
        name: str
    ) -> dict | None:
        """
        Return module
        information.
        """

        return self.modules.get(
            name
        )

    # ---------------------------------- #
    # Dependency Information
    # ---------------------------------- #

    def dependency(
        self,
        file_name: str
    ) -> list[str]:
        """
        Return dependency
        list.
        """

        return self.dependencies.get(
            file_name,
            []
        )

    # ---------------------------------- #
    # Architecture Information
    # ---------------------------------- #

    def architecture_component(
        self,
        component: str
    ) -> dict | None:
        """
        Return architecture
        information.
        """

        return self.architecture.get(
            component
        )

    # ---------------------------------- #
    # Build Knowledge Index
    # ---------------------------------- #

    def build_index(
        self
    ) -> dict:
        """
        Build the complete
        Knowledge Index.
        """

        self.logger.info(
            "Building Knowledge Index."
        )

        index = {

            "knowledge":
            self.knowledge,

            "modules":
            self.modules,

            "dependencies":
            self.dependencies,

            "architecture":
            self.architecture,

        }

        self.logger.success(
            "Knowledge Index built."
        )

        return index
    
    
    
    
        # ---------------------------------- #
    # Knowledge Statistics
    # ---------------------------------- #

    def statistics(
        self
    ) -> dict:
        """
        Return Knowledge
        Index statistics.
        """

        return {

            "knowledge_items":
            len(
                self.knowledge
            ),

            "modules":
            len(
                self.modules
            ),

            "dependencies":
            len(
                self.dependencies
            ),

            "architecture_components":
            len(
                self.architecture
            ),

        }

    # ---------------------------------- #
    # Clear Knowledge
    # ---------------------------------- #

    def clear(
        self
    ) -> None:
        """
        Clear the complete
        Knowledge Index.
        """

        #self.logger.warning(
            #"Clearing Knowledge Index."
        #)

        self.knowledge.clear()

        self.modules.clear()

        self.dependencies.clear()

        self.architecture.clear()

    # ---------------------------------- #
    # Knowledge Exists
    # ---------------------------------- #

    def exists(
        self,
        key: str
    ) -> bool:
        """
        Check whether a
        knowledge item
        exists.
        """

        return (
            key
            in self.knowledge
        )

    # ---------------------------------- #
    # Knowledge Count
    # ---------------------------------- #

    def count(
        self
    ) -> int:
        """
        Return total
        knowledge items.
        """

        return len(
            self.knowledge
        )
    
    
    
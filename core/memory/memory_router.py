"""
File: core/memory/memory_router.py

Purpose:
Central memory access layer.

Routes requests to:

- Episodic Memory
- Working Memory
- Semantic Memory
"""

from core.memory.episodic_memory import (
    EpisodicMemory
)

from core.memory.working_memory import (
    WorkingMemory
)

from core.memory.semantic_memory import (
    SemanticMemory
)


class MemoryRouter:
    """
    Central memory router.
    """

    def __init__(self):
        """
        Initialize memories.
        """

        self.episodic = EpisodicMemory()

        self.working = WorkingMemory()

        self.semantic = SemanticMemory()

    def get_episodic(self):
        """
        Return episodic memory.
        """

        return self.episodic

    def get_working(self):
        """
        Return working memory.
        """

        return self.working

    def get_semantic(self):
        """
        Return semantic memory.
        """

        return self.semantic
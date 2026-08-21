"""
File: core/agents/base_agent.py

Purpose:
Enterprise base agent for KAIROS.

Why:

All future agents should inherit
common capabilities instead of
duplicating code.

Provides:

- Memory access
- Provider access
- Model routing
- Audit logging

Architecture:

BaseAgent
    ↓
PlannerAgent
    ↓
ArchitectAgent
    ↓
CoderAgent
    ↓
DebuggerAgent
    ↓
ReviewerAgent

Future Features:

V2:
- Async execution

V3:
- Parallel execution

V4:
- Agent communication

V5:
- Agent orchestration
"""

# Memory management.
from core.memory.memory_manager import (
    MemoryManager
)

# Provider registry.
from core.llm.provider_manager import (
    ProviderManager
)

# Model selection.
from core.llm.model_router import (
    ModelRouter
)

# Audit logging.
from core.logging.audit_logger import (
    AuditLogger
)



class BaseAgent:
    """
    Enterprise base agent.

    Shared by all future agents.
    """

    def __init__(
        self,
        name: str
    ):
        """
        Initialize agent dependencies.
        """

        self.name = name

        # Shared memory access.
        self.memory = MemoryManager()

        # LLM provider access.
        self.provider_manager = (
            ProviderManager()
        )

        # Model routing layer.
        self.model_router = (
            ModelRouter()
        )

        # Audit logging.
        self.audit_logger = (
            AuditLogger()
        )

    def think(
        self,
        task: str
    ) -> str:
        """
        Agent reasoning placeholder.

        Future:

        Real LLM execution.
        """

        self.audit_logger.log_event(
            "AGENT_THINK",
            f"{self.name} processing task"
        )

        return (
            f"{self.name} processed: "
            f"{task}"
        )

    def get_name(self) -> str:
        """
        Return agent name.
        """

        return self.name
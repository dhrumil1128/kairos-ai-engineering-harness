"""
File: core/agents/agent_manager.py

Purpose:
Central registry for KAIROS agents.

Responsibilities:

- Register agents
- Retrieve agents
- Count agents

Future:

Agent Router
Agent Orchestrator
Parallel Execution
"""

# Memory access.
from core.memory.memory_router import (
    MemoryRouter
)


class AgentManager:
    """
    Central agent registry.
    """

    def __init__(self):
        """
        Initialize manager.
        """

        # Shared memory system.
        self.memory = (
            MemoryRouter()
        )

        # Registered agents.
        self.agents = {}

    def register_agent(
        self,
        name: str,
        agent
    ) -> None:
        """
        Register agent.
        """

        self.agents[name] = agent

    def get_agent(
        self,
        name: str
    ):
        """
        Retrieve agent.
        """

        return self.agents.get(
            name
        )

    def get_agent_count(
        self
    ) -> int:
        """
        Return number of agents.
        """

        return len(
            self.agents
        )

    def list_agents(
        self
    ) -> list[str]:
        """
        Return registered agents.
        """

        return list(
            self.agents.keys()
        )
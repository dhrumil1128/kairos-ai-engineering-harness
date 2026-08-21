"""
File: core/agents/agent_orchestrator.py

Purpose:
Coordinate execution between
multiple KAIROS agents.

Why:

The orchestrator is responsible for:

- Managing agent execution
- Tracking registered agents
- Dispatching messages
- Collecting results

Architecture:

PlannerAgent
      ↓
AgentMessage
      ↓
AgentRouter
      ↓
AgentOrchestrator
      ↓
Target Agents

Future Versions:

V2:
- Async execution

V3:
- Parallel execution

V4:
- Result aggregation

V5:
- Distributed orchestration
"""

# Structured typing.
from typing import Dict, Any


class AgentOrchestrator:
    """
    Central agent coordinator.
    """

    def __init__(self):
        """
        Initialize orchestrator.
        """

        # Registered agents.
        self.agents: Dict[
            str,
            Any
        ] = {}

    def register_agent(
        self,
        name: str,
        agent: Any
    ) -> None:
        """
        Register an agent.

        Parameters:
            name:
                Agent name.

            agent:
                Agent instance.
        """

        self.agents[name] = agent

    def get_agent(
        self,
        name: str
    ) -> Any:
        """
        Retrieve agent.
        """

        return self.agents.get(name)

    def exists(
        self,
        name: str
    ) -> bool:
        """
        Check if agent exists.
        """

        return name in self.agents

    def count(self) -> int:
        """
        Return registered agents.
        """

        return len(self.agents)
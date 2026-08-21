"""
File: core/agents/agent_router.py

Purpose:
Route messages between KAIROS agents.

Why:

Agents should not directly know
about other agents.

The router determines where a
message should go.

Architecture:

Agent
    ↓
AgentMessage
    ↓
AgentRouter
    ↓
Target Agent

Future Versions:

V2:
- Dynamic routing

V3:
- Multi-agent routing

V4:
- Load balancing

V5:
- Distributed agents
"""

# Agent communication object.
from core.agents.agent_message import (
    AgentMessage
)


class AgentRouter:
    """
    Routes messages to agents.
    """

    def __init__(self):
        """
        Initialize routing table.
        """

        self.routes = {
            "PLAN": "ArchitectAgent",
            "CODE": "CoderAgent",
            "SECURITY": "SecurityAgent",
            "RESEARCH": "ResearchAgent",
        }

    def route(
        self,
        message: AgentMessage
    ) -> str:
        """
        Determine target agent.

        Parameters:
            message:
                Agent communication.

        Returns:
            Target agent name.
        """

        return self.routes.get(
            message.message_type,
            "UnknownAgent"
        )

    def add_route(
        self,
        message_type: str,
        agent_name: str
    ) -> None:
        """
        Register routing rule.
        """

        self.routes[
            message_type
        ] = agent_name

    def count(self) -> int:
        """
        Return total routes.
        """

        return len(self.routes)
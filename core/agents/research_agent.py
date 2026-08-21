"""
File: core/agents/research_agent.py

Purpose:
Collect research and knowledge
for KAIROS workflows.

Why:

Many tasks require gathering
information before planning,
coding, or testing.

Architecture:

Research Agent
        ↓
Knowledge Collection
        ↓
Planner Agent

Future Versions:

V2:
- Web search

V3:
- Documentation search

V4:
- MCP integration

V5:
- Autonomous research
"""

from core.agents.base_agent import (
    BaseAgent
)


class ResearchAgent(BaseAgent):
    """
    KAIROS Research Agent.

    Responsible for collecting
    research information.
    """

    def __init__(self):
        """
        Initialize research agent.
        """

        super().__init__(
            name="ResearchAgent"
        )

    def research(
        self,
        topic: str
    ) -> str:
        """
        Perform research.

        Parameters:
            topic:
                Research topic.

        Returns:
            Research summary.
        """

        self.audit_logger.log_event(
            "RESEARCH_COMPLETED",
            f"Research topic: {topic}"
        )

        self.memory.store(
            "latest_research_topic",
            topic
        )

        return (
            f"Research completed for: {topic}"
        )
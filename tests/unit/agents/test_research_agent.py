"""
File: tests/unit/agents/test_research_agent.py

Purpose:
Unit tests for ResearchAgent.
"""

from core.agents.research_agent import (
    ResearchAgent
)


def test_research_agent_creation():
    """
    Verify research agent initialization.
    """

    agent = ResearchAgent()

    assert agent is not None


def test_research_execution():
    """
    Verify research execution.
    """

    agent = ResearchAgent()

    result = agent.research(
        "FastAPI"
    )

    assert (
        "Research completed"
        in result
    )


def test_research_topic_saved():
    """
    Verify topic persistence.
    """

    agent = ResearchAgent()

    topic = "FastAPI"

    agent.research(
        topic
    )

    stored = (
        agent.memory.retrieve(
            "latest_research_topic"
        )
    )

    assert stored == topic


def test_research_audit_event():
    """
    Verify audit logging.
    """

    agent = ResearchAgent()

    agent.research(
        "FastAPI"
    )

    assert (
        agent.audit_logger.count()
        == 1
    )


def test_research_agent_name():
    """
    Verify agent identity.
    """

    agent = ResearchAgent()

    assert (
        agent.get_name()
        == "ResearchAgent"
    )
"""
File:
tests/unit/agents/
test_agent_manager.py

Purpose:
Verify agent manager.
"""

from core.agents.agent_manager import (
    AgentManager
)


class DummyAgent:
    """
    Test agent.
    """

    pass


def test_manager_creation():
    """
    Verify creation.
    """

    manager = (
        AgentManager()
    )

    assert manager is not None


def test_register_agent():
    """
    Verify registration.
    """

    manager = (
        AgentManager()
    )

    manager.register_agent(
        "coder",
        DummyAgent()
    )

    assert (
        manager.get_agent_count()
        == 1
    )


def test_get_agent():
    """
    Verify retrieval.
    """

    manager = (
        AgentManager()
    )

    agent = DummyAgent()

    manager.register_agent(
        "coder",
        agent
    )

    assert (
        manager.get_agent(
            "coder"
        )
        == agent
    )


def test_list_agents():
    """
    Verify listing.
    """

    manager = (
        AgentManager()
    )

    manager.register_agent(
        "coder",
        DummyAgent()
    )

    agents = (
        manager.list_agents()
    )

    assert (
        "coder"
        in agents
    )
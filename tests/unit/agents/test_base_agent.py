"""
File: tests/unit/agents/test_base_agent.py

Purpose:
Unit tests for BaseAgent.

Why:
Verify agent initialization,
reasoning, and shared services.

Architecture:

BaseAgent
    ↓
Future Agents
"""

# Agent under test.
from core.agents.base_agent import (
    BaseAgent
)


def test_agent_creation():
    """
    Verify agent initialization.
    """

    agent = BaseAgent(
        name="PlannerAgent"
    )

    assert agent is not None


def test_agent_name():
    """
    Verify agent naming.
    """

    agent = BaseAgent(
        name="PlannerAgent"
    )

    assert (
        agent.get_name()
        == "PlannerAgent"
    )


def test_agent_think():
    """
    Verify reasoning placeholder.
    """

    agent = BaseAgent(
        name="PlannerAgent"
    )

    result = agent.think(
        "Build authentication"
    )

    assert (
        "processed"
        in result
    )


def test_memory_available():
    """
    Verify memory service exists.
    """

    agent = BaseAgent(
        name="PlannerAgent"
    )

    assert agent.memory is not None


def test_provider_manager_available():
    """
    Verify provider manager exists.
    """

    agent = BaseAgent(
        name="PlannerAgent"
    )

    assert (
        agent.provider_manager
        is not None
    )


def test_model_router_available():
    """
    Verify model router exists.
    """

    agent = BaseAgent(
        name="PlannerAgent"
    )

    assert (
        agent.model_router
        is not None
    )


def test_audit_logger_available():
    """
    Verify audit logger exists.
    """

    agent = BaseAgent(
        name="PlannerAgent"
    )

    assert (
        agent.audit_logger
        is not None
    )
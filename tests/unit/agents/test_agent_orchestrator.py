"""
File: tests/unit/agents/test_agent_orchestrator.py

Purpose:
Unit tests for AgentOrchestrator.
"""

from core.agents.agent_orchestrator import (
    AgentOrchestrator
)

from core.agents.planner_agent import (
    PlannerAgent
)


def test_orchestrator_creation():
    """
    Verify orchestrator initialization.
    """

    orchestrator = AgentOrchestrator()

    assert orchestrator is not None


def test_register_agent():
    """
    Verify agent registration.
    """

    orchestrator = AgentOrchestrator()

    planner = PlannerAgent()

    orchestrator.register_agent(
        "PlannerAgent",
        planner
    )

    assert orchestrator.count() == 1


def test_get_agent():
    """
    Verify agent retrieval.
    """

    orchestrator = AgentOrchestrator()

    planner = PlannerAgent()

    orchestrator.register_agent(
        "PlannerAgent",
        planner
    )

    result = orchestrator.get_agent(
        "PlannerAgent"
    )

    assert result == planner


def test_agent_exists():
    """
    Verify existence check.
    """

    orchestrator = AgentOrchestrator()

    planner = PlannerAgent()

    orchestrator.register_agent(
        "PlannerAgent",
        planner
    )

    assert (
        orchestrator.exists(
            "PlannerAgent"
        )
        is True
    )


def test_missing_agent():
    """
    Verify missing agent lookup.
    """

    orchestrator = AgentOrchestrator()

    assert (
        orchestrator.get_agent(
            "UnknownAgent"
        )
        is None
    )
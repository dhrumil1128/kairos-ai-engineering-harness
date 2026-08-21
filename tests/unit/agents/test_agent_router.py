"""
File: tests/unit/agents/test_agent_router.py

Purpose:
Unit tests for AgentRouter.
"""

from core.agents.agent_router import (
    AgentRouter
)

from core.agents.agent_message import (
    AgentMessage
)


def test_router_creation():
    """
    Verify router initialization.
    """

    router = AgentRouter()

    assert router is not None


def test_plan_route():
    """
    Verify PLAN routing.
    """

    router = AgentRouter()

    message = AgentMessage(
        sender="PlannerAgent",
        receiver="",
        message_type="PLAN",
        payload=[]
    )

    assert (
        router.route(message)
        == "ArchitectAgent"
    )


def test_add_route():
    """
    Verify custom route creation.
    """

    router = AgentRouter()

    router.add_route(
        "TEST",
        "TesterAgent"
    )

    message = AgentMessage(
        sender="PlannerAgent",
        receiver="",
        message_type="TEST",
        payload=[]
    )

    assert (
        router.route(message)
        == "TesterAgent"
    )


def test_unknown_route():
    """
    Verify fallback route.
    """

    router = AgentRouter()

    message = AgentMessage(
        sender="PlannerAgent",
        receiver="",
        message_type="UNKNOWN",
        payload=[]
    )

    assert (
        router.route(message)
        == "UnknownAgent"
    )


def test_route_count():
    """
    Verify route count.
    """

    router = AgentRouter()

    assert router.count() == 4
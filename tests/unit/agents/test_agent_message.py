"""
File: tests/unit/agents/test_agent_message.py

Purpose:
Unit tests for AgentMessage.
"""

from core.agents.agent_message import (
    AgentMessage
)


def test_message_creation():
    """
    Verify message creation.
    """

    message = AgentMessage(
        sender="PlannerAgent",
        receiver="ArchitectAgent",
        message_type="PLAN",
        payload=["Task 1"]
    )

    assert message is not None


def test_sender():
    """
    Verify sender field.
    """

    message = AgentMessage(
        sender="PlannerAgent",
        receiver="ArchitectAgent",
        message_type="PLAN",
        payload=[]
    )

    assert (
        message.sender
        == "PlannerAgent"
    )


def test_receiver():
    """
    Verify receiver field.
    """

    message = AgentMessage(
        sender="PlannerAgent",
        receiver="ArchitectAgent",
        message_type="PLAN",
        payload=[]
    )

    assert (
        message.receiver
        == "ArchitectAgent"
    )


def test_message_type():
    """
    Verify message type.
    """

    message = AgentMessage(
        sender="PlannerAgent",
        receiver="ArchitectAgent",
        message_type="PLAN",
        payload=[]
    )

    assert (
        message.message_type
        == "PLAN"
    )


def test_payload():
    """
    Verify payload.
    """

    payload = [
        "Task 1",
        "Task 2"
    ]

    message = AgentMessage(
        sender="PlannerAgent",
        receiver="ArchitectAgent",
        message_type="PLAN",
        payload=payload
    )

    assert (
        message.payload
        == payload
    )
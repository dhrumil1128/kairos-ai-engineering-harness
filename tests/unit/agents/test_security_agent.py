"""
File: tests/unit/agents/test_security_agent.py

Purpose:
Unit tests for SecurityAgent.
"""

from core.agents.security_agent import (
    SecurityAgent
)


def test_security_agent_creation():
    """
    Verify security agent initialization.
    """

    agent = SecurityAgent()

    assert agent is not None


def test_security_analysis():
    """
    Verify security analysis.
    """

    agent = SecurityAgent()

    result = agent.analyze_security(
        "print('hello')"
    )

    assert (
        "Security"
        in result
    )


def test_security_target_saved():
    """
    Verify target persistence.
    """

    agent = SecurityAgent()

    code = "print('hello')"

    agent.analyze_security(
        code
    )

    stored = (
        agent.memory.retrieve(
            "latest_security_target"
        )
    )

    assert stored == code


def test_security_audit_event():
    """
    Verify audit logging.
    """

    agent = SecurityAgent()

    agent.analyze_security(
        "print('hello')"
    )

    assert (
        agent.audit_logger.count()
        == 1
    )


def test_security_agent_name():
    """
    Verify agent identity.
    """

    agent = SecurityAgent()

    assert (
        agent.get_name()
        == "SecurityAgent"
    )
"""
File: tests/unit/agents/test_tester_agent.py

Purpose:
Unit tests for TesterAgent.
"""

from core.agents.tester_agent import (
    TesterAgent
)


def test_agent_creation():

    agent = (
        TesterAgent()
    )

    assert (
        agent is not None
    )


def test_provider_manager_exists():

    agent = (
        TesterAgent()
    )

    assert hasattr(
        agent,
        "provider_manager"
    )


def test_run_tests_returns_dict():

    agent = (
        TesterAgent()
    )

    result = (
        agent.run_tests(
            {
                "status": "reviewed"
            }
        )
    )

    assert isinstance(
        result,
        dict
    )


def test_test_status():

    agent = (
        TesterAgent()
    )

    result = (
        agent.run_tests(
            {
                "status": "reviewed"
            }
        )
    )

    assert (
        result["status"]
        == "tested"
    )


def test_generated_test_report_exists():

    agent = (
        TesterAgent()
    )

    result = (
        agent.run_tests(
            {
                "status": "reviewed"
            }
        )
    )

    assert (
        "generated_test_report"
        in result
    )


def test_review_exists():

    agent = (
        TesterAgent()
    )

    review = {
        "status": "reviewed"
    }

    result = (
        agent.run_tests(
            review
        )
    )

    assert (
        "review"
        in result
    )
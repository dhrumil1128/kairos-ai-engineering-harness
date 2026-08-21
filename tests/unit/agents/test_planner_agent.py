"""
File: tests/unit/agents/test_planner_agent.py

Purpose:
Unit tests for PlannerAgent.

Why:
Verify planning behavior,
memory integration,
and audit logging.

Architecture:

User Goal
    ↓
Planner Agent
    ↓
Task Plan
"""

# Agent under test.
from core.agents.planner_agent import (
    PlannerAgent
)


class StubProviderManager:
    def __init__(
        self,
        response
    ):
        self.response = response
        self.calls = []

    def execute(
        self,
        task_type: str,
        prompt: str
    ):
        self.calls.append(
            {
                "task_type": task_type,
                "prompt": prompt,
            }
        )

        return self.response


def make_planner(
    response="Plan the implementation."
) -> PlannerAgent:
    planner = PlannerAgent()
    planner.provider_manager = StubProviderManager(
        response
    )

    return planner


def test_planner_creation():
    """
    Verify planner initialization.
    """

    planner = PlannerAgent()

    assert planner is not None


def test_create_plan():
    """
    Verify plan generation.
    """

    planner = make_planner()

    plan = planner.create_plan(
        "Build authentication system"
    )

    assert (
    plan["status"]
    == "planned"
)


def test_goal_saved_to_memory():
    """
    Verify goal persistence.
    """

    planner = make_planner()

    goal = "Build authentication system"

    planner.create_plan(goal)

    stored_plan = (
    planner.memory.retrieve(
        "latest_plan"
    )
)

    assert (
        stored_plan["task"]
        == goal
    )


def test_audit_event_created():
    """
    Verify audit event creation.
    """

    planner = make_planner()

    planner.create_plan(
        "Build authentication system"
    )

    assert (
        planner.audit_logger.count()
        == 1
    )


def test_plan_contains_analysis():
    """
    Verify first planning step.
    """

    planner = make_planner()

    plan = planner.create_plan(
        "Build authentication system"
    )

    assert (
    plan["next_agent"]
    == "ArchitectAgent"
)
    
    
def test_provider_manager_exists():

    planner = (
        PlannerAgent()
    )

    assert hasattr(
        planner,
        "provider_manager"
    )


def test_plain_text_provider_response_is_preserved():
    """
    Verify plain text responses remain available to downstream agents.
    """

    planner = make_planner(
        "Analyze, design, implement, and test."
    )

    plan = planner.create_plan(
        "Build authentication system"
    )

    assert (
        plan["generated_plan"]
        == "Analyze, design, implement, and test."
    )


def test_parsed_dict_provider_response_is_preserved():
    """
    Verify provider-layer parsed dicts are not reparsed or stringified.
    """

    generated_plan = {
        "steps": [
            "Analyze",
            "Design",
            "Implement",
        ],
        "risks": [],
    }

    planner = make_planner(
        generated_plan
    )

    plan = planner.create_plan(
        "Build authentication system"
    )

    assert (
        plan["generated_plan"]
        is generated_plan
    )


def test_parsed_list_provider_response_is_preserved():
    """
    Verify provider-layer parsed lists are supported.
    """

    generated_plan = [
        "Analyze",
        "Design",
        "Implement",
    ]

    planner = make_planner(
        generated_plan
    )

    plan = planner.create_plan(
        "Build authentication system"
    )

    assert (
        plan["generated_plan"]
        is generated_plan
    )


def test_provider_called_for_planning_task():
    """
    Verify provider execution behavior is unchanged.
    """

    planner = make_planner()

    planner.create_plan(
        "Build authentication system"
    )

    assert (
        planner.provider_manager.calls[0]["task_type"]
        == "planning"
    )

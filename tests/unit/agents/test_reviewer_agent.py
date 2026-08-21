"""
File: tests/unit/agents/test_reviewer_agent.py

Purpose:
Unit tests for ReviewerAgent.
"""

from core.agents.reviewer_agent import (
    ReviewerAgent
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


def make_agent(
    response="Looks good."
) -> ReviewerAgent:
    agent = ReviewerAgent()
    agent.provider_manager = StubProviderManager(
        response
    )

    return agent


def make_implementation() -> dict:
    return {
        "status": "generated",
        "implementation_spec": {
            "files": [
                {
                    "path": "src/main.py",
                    "content": "print('hello')",
                }
            ]
        },
    }


def test_agent_creation():
    """
    Verify creation.
    """

    agent = (
        ReviewerAgent()
    )

    assert (
        agent is not None
    )


def test_provider_manager_exists():
    """
    Verify provider manager.
    """

    agent = (
        ReviewerAgent()
    )

    assert hasattr(
        agent,
        "provider_manager"
    )


def test_review_returns_dict():
    """
    Verify review output.
    """

    agent = make_agent()

    result = (
        agent.review_code(
            make_implementation()
        )
    )

    assert isinstance(
        result,
        dict
    )


def test_review_status():
    """
    Verify review status.
    """

    agent = make_agent()

    result = (
        agent.review_code(
            make_implementation()
        )
    )

    assert (
        result["status"]
        == "reviewed"
    )


def test_generated_review_exists():
    """
    Verify generated review.
    """

    agent = make_agent()

    result = (
        agent.review_code(
            make_implementation()
        )
    )

    assert (
        "generated_review"
        in result
    )


def test_implementation_exists():
    """
    Verify implementation.
    """

    agent = make_agent()

    implementation = make_implementation()

    result = (
        agent.review_code(
            implementation
        )
    )

    assert (
        "implementation"
        in result
    )


def test_plain_text_provider_response_is_preserved():
    """
    Verify plain text review responses remain unchanged.
    """

    agent = make_agent(
        "No issues found."
    )

    result = agent.review_code(
        make_implementation()
    )

    assert (
        result["generated_review"]
        == "No issues found."
    )


def test_parsed_dict_provider_response_is_preserved():
    """
    Verify provider-layer parsed dict reviews are not reparsed or stringified.
    """

    review_response = {
        "issues": [],
        "overall_status": "approved",
    }

    agent = make_agent(
        review_response
    )

    result = agent.review_code(
        make_implementation()
    )

    assert (
        result["generated_review"]
        is review_response
    )


def test_parsed_list_provider_response_is_preserved():
    """
    Verify provider-layer parsed list reviews are supported.
    """

    review_response = [
        {
            "severity": "low",
            "message": "Add more docs.",
        }
    ]

    agent = make_agent(
        review_response
    )

    result = agent.review_code(
        make_implementation()
    )

    assert (
        result["generated_review"]
        is review_response
    )


def test_memory_and_audit_behavior_preserved():
    """
    Verify existing side effects are preserved.
    """

    agent = make_agent()
    implementation = make_implementation()

    result = agent.review_code(
        implementation
    )

    assert (
        agent.memory.retrieve("latest_review_target")
        == implementation
    )
    assert (
        agent.memory.retrieve("latest_review")
        == result
    )
    assert (
        agent.audit_logger.count()
        == 1
    )


def test_provider_called_for_review_task():
    """
    Verify provider execution behavior is unchanged.
    """

    agent = make_agent()

    agent.review_code(
        make_implementation()
    )

    assert (
        agent.provider_manager.calls[0]["task_type"]
        == "review"
    )


def test_accepted_review_with_no_critical_issues_is_approved():
    """
    Verify non-blocking accepted text does not trigger repair.
    """

    agent = make_agent(
        "- Overall Status: Accepted\n"
        "- No critical issues detected\n"
        "- Minor improvements remain optional"
    )

    result = agent.review_code(
        make_implementation()
    )

    assert result["approved"] is True


def test_accepted_with_minor_improvements_is_approved():
    """
    Verify minor improvements are non-blocking.
    """

    agent = make_agent(
        "Overall Status: Accepted with Minor Improvements\n"
        "Severity: Low\n"
        "Recommendation: Add a README example."
    )

    result = agent.review_code(
        make_implementation()
    )

    assert result["approved"] is True


def test_optional_recommendations_do_not_block_review():
    """
    Verify optional recommendations do not trigger repair.
    """

    agent = make_agent(
        "No blocking issues found.\n"
        "Optional recommendation: add more comments."
    )

    result = agent.review_code(
        make_implementation()
    )

    assert result["approved"] is True


def test_high_severity_issue_blocks_review():
    """
    Verify High severity issues trigger repair.
    """

    agent = make_agent(
        "Issues Found:\n"
        "- Missing required import\n"
        "Severity: High\n"
        "Overall Status: Changes Requested"
    )

    result = agent.review_code(
        make_implementation()
    )

    assert result["approved"] is False


def test_structured_accepted_status_overrides_inconsistent_approved_false():
    """
    Verify explicit accepted conclusion is the source of truth.
    """

    agent = make_agent(
        {
            "approved": False,
            "overall_status": "Accepted with Minor Improvements",
            "issues": [
                {
                    "severity": "low",
                    "message": "Optional docs improvement.",
                }
            ],
        }
    )

    result = agent.review_code(
        make_implementation()
    )

    assert result["approved"] is True

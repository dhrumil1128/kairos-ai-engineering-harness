"""
File:
tests/unit/orchestration/
test_execution_loop.py

Purpose:
Verify execution loop.
"""

from core.orchestration.execution_loop import (
    ExecutionLoop
)


def test_retry_response():
    """
    Verify retry workflow.
    """

    loop = (
        ExecutionLoop()
    )

    result = (
        loop.process_error(
            "SyntaxError",
            1
        )
    )

    assert (
        result["status"]
        == "retry"
    )


def test_analysis_exists():
    """
    Verify analysis output.
    """

    loop = (
        ExecutionLoop()
    )

    result = (
        loop.process_error(
            "ImportError",
            1
        )
    )

    assert (
        "analysis"
        in result
    )


def test_repair_plan_exists():
    """
    Verify repair plan output.
    """

    loop = (
        ExecutionLoop()
    )

    result = (
        loop.process_error(
            "SyntaxError",
            1
        )
    )

    assert (
        "repair_plan"
        in result
    )


def test_retry_limit():
    """
    Verify retry limit.
    """

    loop = (
        ExecutionLoop()
    )

    result = (
        loop.process_error(
            "SyntaxError",
            3
        )
    )

    assert (
        result["status"]
        == "failed"
    )
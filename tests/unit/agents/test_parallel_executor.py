"""
File: tests/unit/agents/test_parallel_executor.py

Purpose:
Unit tests for ParallelExecutor.

Why:
Verify task execution and
result collection.

Architecture:

Agent Orchestrator
        ↓
Parallel Executor
        ↓
Task Results
"""

# Executor under test.
from core.agents.parallel_executor import (
    ParallelExecutor
)


def test_executor_creation():
    """
    Verify executor initialization.
    """

    executor = ParallelExecutor()

    assert executor is not None


def test_single_task_execution():
    """
    Verify one task execution.
    """

    executor = ParallelExecutor()

    def task():
        return "success"

    results = executor.execute(
        [task]
    )

    assert results == ["success"]


def test_multiple_task_execution():
    """
    Verify multiple task execution.
    """

    executor = ParallelExecutor()

    def task_one():
        return "task_one"

    def task_two():
        return "task_two"

    results = executor.execute(
        [
            task_one,
            task_two
        ]
    )

    assert len(results) == 2


def test_result_order():
    """
    Verify result collection.
    """

    executor = ParallelExecutor()

    def first():
        return 1

    def second():
        return 2

    results = executor.execute(
        [
            first,
            second
        ]
    )

    assert results == [1, 2]


def test_empty_task_list():
    """
    Verify empty execution.
    """

    executor = ParallelExecutor()

    results = executor.execute([])

    assert results == []
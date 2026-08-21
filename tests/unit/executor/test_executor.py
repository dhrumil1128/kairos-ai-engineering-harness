"""
File: tests/unit/executor/test_executor.py

Purpose:
Unit tests for KAIROS Executor.

Why:
Verify the execution layer behaves correctly
before integrating it with the Recursive Engine.

Architecture:

Task
 ↓
Executor
 ↓
Execution Result
"""

# Execution layer under test.
from core.executor.executor import Executor

# Shared task contract.
from core.shared.schemas import TaskSchema


def test_executor_creation():
    """
    Verify executor can be instantiated.
    """

    executor = Executor()

    assert executor is not None


def test_task_execution():
    """
    Verify executor successfully executes a task.
    """

    task = TaskSchema(
        name="Build API"
    )

    executor = Executor()

    result = executor.execute(task)

    assert result is True
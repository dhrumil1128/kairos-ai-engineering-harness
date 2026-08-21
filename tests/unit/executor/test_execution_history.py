"""
File: tests/unit/executor/test_execution_history.py

Purpose:
Unit tests for ExecutionHistory.

Why:
Verify execution records are stored correctly.

Architecture:

Executor
    ↓
Execution History
    ↓
Unit Tests
"""

# Execution history layer under test.
from core.executor.execution_history import (
    ExecutionHistory
)


def test_execution_history_creation():
    """
    Verify history initialization.
    """

    history = ExecutionHistory()

    assert history is not None


def test_add_record():
    """
    Verify record storage.
    """

    history = ExecutionHistory()

    history.add_record(
        task_id="task_001",
        command="echo hello",
        success=True,
        return_code=0,
    )

    assert history.count() == 1


def test_get_records():
    """
    Verify record retrieval.
    """

    history = ExecutionHistory()

    history.add_record(
        task_id="task_001",
        command="echo hello",
        success=True,
        return_code=0,
    )

    records = history.get_records()

    assert len(records) == 1

    assert records[0]["task_id"] == "task_001"

    assert records[0]["command"] == "echo hello"


def test_count():
    """
    Verify record counting.
    """

    history = ExecutionHistory()

    history.add_record(
        task_id="1",
        command="echo 1",
        success=True,
        return_code=0,
    )

    history.add_record(
        task_id="2",
        command="echo 2",
        success=True,
        return_code=0,
    )

    assert history.count() == 2
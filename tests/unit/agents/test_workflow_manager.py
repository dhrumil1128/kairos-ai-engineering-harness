"""
File: tests/unit/agents/test_workflow_manager.py

Purpose:
Unit tests for WorkflowManager.
"""

from core.agents.workflow_manager import (
    WorkflowManager
)


def test_workflow_creation():
    """
    Verify workflow initialization.
    """

    workflow = WorkflowManager()

    assert workflow is not None


def test_add_task():
    """
    Verify task addition.
    """

    workflow = WorkflowManager()

    workflow.add_task(
        "Design System"
    )

    assert (
        workflow.count()
        == 1
    )


def test_get_tasks():
    """
    Verify task retrieval.
    """

    workflow = WorkflowManager()

    workflow.add_task(
        "Design System"
    )

    tasks = (
        workflow.get_tasks()
    )

    assert (
        tasks[0]
        == "Design System"
    )


def test_clear_workflow():
    """
    Verify workflow clearing.
    """

    workflow = WorkflowManager()

    workflow.add_task(
        "Task A"
    )

    workflow.clear()

    assert (
        workflow.count()
        == 0
    )


def test_multiple_tasks():
    """
    Verify multiple task handling.
    """

    workflow = WorkflowManager()

    workflow.add_task(
        "Task A"
    )

    workflow.add_task(
        "Task B"
    )

    workflow.add_task(
        "Task C"
    )

    assert (
        workflow.count()
        == 3
    )
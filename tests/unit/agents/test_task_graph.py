"""
File: tests/unit/agents/test_task_graph.py

Purpose:
Unit tests for TaskGraph.

Why:
Verify task registration,
dependency tracking,
and graph management.

Architecture:

Planner Agent
        ↓
Task Graph
        ↓
Execution Engine
"""

from core.agents.task_graph import (
    TaskGraph
)


def test_graph_creation():
    """
    Verify graph initialization.
    """

    graph = TaskGraph()

    assert graph is not None


def test_add_task():
    """
    Verify task registration.
    """

    graph = TaskGraph()

    graph.add_task(
        "design"
    )

    assert graph.exists(
        "design"
    ) is True


def test_add_task_with_dependencies():
    """
    Verify dependency storage.
    """

    graph = TaskGraph()

    graph.add_task(
        "backend",
        [
            "design",
            "database"
        ]
    )

    dependencies = (
        graph.get_dependencies(
            "backend"
        )
    )

    assert len(
        dependencies
    ) == 2


def test_get_dependencies():
    """
    Verify dependency retrieval.
    """

    graph = TaskGraph()

    graph.add_task(
        "testing",
        [
            "backend",
            "frontend"
        ]
    )

    assert (
        graph.get_dependencies(
            "testing"
        )
        == [
            "backend",
            "frontend"
        ]
    )


def test_task_count():
    """
    Verify graph count.
    """

    graph = TaskGraph()

    graph.add_task(
        "design"
    )

    graph.add_task(
        "backend"
    )

    assert (
        graph.count()
        == 2
    )
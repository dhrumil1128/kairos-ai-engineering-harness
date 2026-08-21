"""
File: tests/unit/shared/test_schemas.py

Purpose:
Unit tests for KAIROS schemas.

Why:
Ensures schema validation and default values
work correctly before other modules depend on them.

Architecture:

TaskSchema
     ↓
Unit Tests
"""

# Core task schema under test.
from core.shared.schemas import TaskSchema

# Standard task status definitions.
from core.shared.enums import TaskStatus


def test_task_creation():
    """
    Verify a task can be created successfully.
    """

    task = TaskSchema(
        name="Build API",
        description="Create FastAPI backend"
    )

    assert task.name == "Build API"
    assert task.description == "Create FastAPI backend"


def test_default_status():
    """
    Verify default status is PENDING.
    """

    task = TaskSchema(name="Test Task")

    assert task.status == TaskStatus.PENDING


def test_default_priority():
    """
    Verify default priority value.
    """

    task = TaskSchema(name="Test Task")

    assert task.priority == 1


def test_uuid_generation():
    """
    Verify automatic ID generation.
    """

    task = TaskSchema(name="Test Task")

    assert task.id is not None
    assert len(task.id) > 0


def test_timestamp_generation():
    """
    Verify timestamps are generated.
    """

    task = TaskSchema(name="Test Task")

    assert task.created_at is not None
    assert task.updated_at is not None


def test_custom_status():
    """
    Verify custom status assignment.
    """

    task = TaskSchema(
        name="Test Task",
        status=TaskStatus.RUNNING
    )

    assert task.status == TaskStatus.RUNNING
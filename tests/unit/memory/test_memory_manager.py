"""
File: tests/unit/memory/test_memory_manager.py

Purpose:
Unit tests for MemoryManager.

Why:
Verify memory storage, retrieval,
deletion, and counting.

Architecture:

Agents
    ↓
Memory Manager
    ↓
Memory Store
"""

# Memory layer under test.
from core.memory.memory_manager import (
    MemoryManager
)


def test_memory_manager_creation():
    """
    Verify memory manager initialization.
    """

    memory = MemoryManager()

    assert memory is not None


def test_store_memory():
    """
    Verify memory storage.
    """

    memory = MemoryManager()

    memory.store(
        "project",
        "KAIROS"
    )

    assert memory.retrieve(
        "project"
    ) == "KAIROS"


def test_retrieve_memory():
    """
    Verify memory retrieval.
    """

    memory = MemoryManager()

    memory.store(
        "task",
        "Build API"
    )

    result = memory.retrieve(
        "task"
    )

    assert result == "Build API"


def test_delete_memory():
    """
    Verify memory deletion.
    """

    memory = MemoryManager()

    memory.store(
        "temp",
        "value"
    )

    memory.delete("temp")

    assert memory.retrieve(
        "temp"
    ) is None


def test_exists():
    """
    Verify existence checks.
    """

    memory = MemoryManager()

    memory.store(
        "agent",
        "planner"
    )

    assert memory.exists(
        "agent"
    ) is True

    assert memory.exists(
        "missing"
    ) is False


def test_count():
    """
    Verify memory counting.
    """

    memory = MemoryManager()

    memory.store(
        "one",
        "1"
    )

    memory.store(
        "two",
        "2"
    )

    assert memory.count() == 2
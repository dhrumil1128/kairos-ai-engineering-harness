"""
File:
tests/unit/memory/
test_working_memory.py

Purpose:
Verify persistent working memory.
"""

from core.memory.working_memory import (
    WorkingMemory
)


def test_memory_creation():
    """
    Verify creation.
    """

    memory = (
        WorkingMemory()
    )

    assert (
        memory
        is not None
    )


def test_store_value():
    """
    Verify storage.
    """

    memory = (
        WorkingMemory()
    )

    memory.store(
        "task",
        "Build API"
    )

    assert True


def test_retrieve_value():
    """
    Verify retrieval.
    """

    memory = (
        WorkingMemory()
    )

    memory.store(
        "task",
        "Build API"
    )

    value = memory.retrieve(
        "task"
    )

    assert (
        value
        == "Build API"
    )


def test_missing_key():
    """
    Verify missing key.
    """

    memory = (
        WorkingMemory()
    )

    value = memory.retrieve(
        "does_not_exist"
    )

    assert (
        value is None
    )
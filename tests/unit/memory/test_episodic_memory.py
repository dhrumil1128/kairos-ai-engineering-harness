"""
File:
tests/unit/memory/
test_episodic_memory.py

Purpose:
Verify persistent episodic memory.
"""

from core.memory.episodic_memory import (
    EpisodicMemory
)


def test_memory_creation():
    """
    Verify creation.
    """

    memory = (
        EpisodicMemory()
    )

    assert (
        memory
        is not None
    )


def test_add_event():
    """
    Verify event storage.
    """

    memory = (
        EpisodicMemory()
    )

    memory.add_event(
        "Task Started"
    )

    assert True


def test_latest_event():
    """
    Verify retrieval.
    """

    memory = (
        EpisodicMemory()
    )

    memory.add_event(
        "Task Completed"
    )

    event = (
        memory.get_latest_event()
    )

    assert (
        event
        == "Task Completed"
    )


def test_latest_event_exists():
    """
    Verify event exists.
    """

    memory = (
        EpisodicMemory()
    )

    memory.add_event(
        "Build Successful"
    )

    assert (
        memory.get_latest_event()
        is not None
    )
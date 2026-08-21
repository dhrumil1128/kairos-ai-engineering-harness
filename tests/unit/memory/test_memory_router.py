"""
File:
tests/unit/memory/
test_memory_router.py

Purpose:
Verify memory router.
"""

from core.memory.memory_router import (
    MemoryRouter
)


def test_router_creation():
    """
    Verify router creation.
    """

    router = MemoryRouter()

    assert router is not None


def test_episodic_access():
    """
    Verify episodic access.
    """

    router = MemoryRouter()

    assert (
        router.get_episodic()
        is not None
    )


def test_working_access():
    """
    Verify working access.
    """

    router = MemoryRouter()

    assert (
        router.get_working()
        is not None
    )


def test_semantic_access():
    """
    Verify semantic access.
    """

    router = MemoryRouter()

    assert (
        router.get_semantic()
        is not None
    )
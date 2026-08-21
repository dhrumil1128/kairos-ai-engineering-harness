"""
File: tests/unit/context/test_knowledge_manager.py

Purpose:
Unit tests for KnowledgeManager.
"""

from core.context.knowledge_manager import (
    KnowledgeManager
)


def test_manager_creation():
    """
    Verify initialization.
    """

    manager = KnowledgeManager()

    assert manager is not None


def test_store_knowledge():
    """
    Verify storage.
    """

    manager = KnowledgeManager()

    manager.store(
        "project",
        "KAIROS"
    )

    assert (
        manager.retrieve(
            "project"
        )
        == "KAIROS"
    )


def test_exists():
    """
    Verify existence.
    """

    manager = KnowledgeManager()

    manager.store(
        "key",
        "value"
    )

    assert (
        manager.exists(
            "key"
        )
        is True
    )


def test_count():
    """
    Verify item count.
    """

    manager = KnowledgeManager()

    manager.store(
        "a",
        "1"
    )

    manager.store(
        "b",
        "2"
    )

    assert (
        manager.count()
        == 2
    )


def test_clear():
    """
    Verify clear operation.
    """

    manager = KnowledgeManager()

    manager.store(
        "a",
        "1"
    )

    manager.clear()

    assert (
        manager.count()
        == 0
    )
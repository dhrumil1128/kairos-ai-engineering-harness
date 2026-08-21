"""
File: tests/unit/context/test_project_context.py

Purpose:
Unit tests for ProjectContext.
"""

from core.context.project_context import (
    ProjectContext
)


def test_context_creation():
    """
    Verify initialization.
    """

    context = ProjectContext()

    assert context is not None


def test_add_document():
    """
    Verify document storage.
    """

    context = ProjectContext()

    context.add_document(
        "README.md",
        "Project Info"
    )

    assert (
        context.document_exists(
            "README.md"
        )
        is True
    )


def test_get_document():
    """
    Verify retrieval.
    """

    context = ProjectContext()

    context.add_document(
        "README.md",
        "Project Info"
    )

    assert (
        context.get_document(
            "README.md"
        )
        == "Project Info"
    )


def test_document_count():
    """
    Verify count.
    """

    context = ProjectContext()

    context.add_document(
        "A.md",
        "A"
    )

    context.add_document(
        "B.md",
        "B"
    )

    assert (
        context.document_count()
        == 2
    )


def test_all_documents():
    """
    Verify document listing.
    """

    context = ProjectContext()

    context.add_document(
        "README.md",
        "Project"
    )

    docs = (
        context.all_documents()
    )

    assert (
        "README.md"
        in docs
    )
"""
File: tests/unit/context/test_context_pipeline.py

Purpose:
Unit tests for ContextPipeline.
"""

from core.context.context_pipeline import (
    ContextPipeline
)


def test_pipeline_creation():
    pipeline = ContextPipeline()

    assert pipeline is not None


def test_add_document():
    pipeline = ContextPipeline()

    pipeline.add_document(
        "README.md",
        "Project"
    )

    assert (
        pipeline.document_count()
        == 1
    )


def test_get_context():
    pipeline = ContextPipeline()

    pipeline.add_document(
        "README.md",
        "Project"
    )

    context = (
        pipeline.get_context()
    )

    assert (
        "README.md"
        in context
    )


def test_multiple_documents():
    pipeline = ContextPipeline()

    pipeline.add_document(
        "README.md",
        "A"
    )

    pipeline.add_document(
        "TASKS.md",
        "B"
    )

    assert (
        pipeline.document_count()
        == 2
    )


def test_empty_context():
    pipeline = ContextPipeline()

    assert (
        pipeline.get_context()
        == {}
    )
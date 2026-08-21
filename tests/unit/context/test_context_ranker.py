"""
File: tests/unit/context/test_context_ranker.py

Purpose:
Unit tests for ContextRanker.
"""

from core.context.context_ranker import (
    ContextRanker
)


def test_ranker_creation():
    """
    Verify initialization.
    """

    ranker = ContextRanker()

    assert ranker is not None


def test_rank_context():
    """
    Verify ranking.
    """

    ranker = ContextRanker()

    contexts = [
        "FastAPI backend service",
        "React frontend",
        "Database schema"
    ]

    result = ranker.rank(
        contexts,
        "FastAPI"
    )

    assert (
        result[0]
        == "FastAPI backend service"
    )


def test_top_k():
    """
    Verify top-k retrieval.
    """

    ranker = ContextRanker()

    contexts = [
        "FastAPI backend",
        "React frontend",
        "Database"
    ]

    result = ranker.top_k(
        contexts,
        "FastAPI",
        1
    )

    assert len(result) == 1


def test_empty_context():
    """
    Verify empty input.
    """

    ranker = ContextRanker()

    result = ranker.rank(
        [],
        "FastAPI"
    )

    assert result == []


def test_no_match():
    """
    Verify unmatched query.
    """

    ranker = ContextRanker()

    contexts = [
        "Database"
    ]

    result = ranker.rank(
        contexts,
        "FastAPI"
    )

    assert len(result) == 1
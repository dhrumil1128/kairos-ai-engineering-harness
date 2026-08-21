"""
File: tests/unit/context/test_token_optimizer.py

Purpose:
Unit tests for TokenOptimizer.
"""

from core.context.token_optimizer import (
    TokenOptimizer
)


def test_optimizer_creation():
    """
    Verify initialization.
    """

    optimizer = TokenOptimizer()

    assert optimizer is not None


def test_token_estimation():
    """
    Verify token estimation.
    """

    optimizer = TokenOptimizer()

    tokens = (
        optimizer.estimate_tokens(
            "hello world"
        )
    )

    assert tokens > 0


def test_empty_text():
    """
    Verify empty text.
    """

    optimizer = TokenOptimizer()

    assert (
        optimizer.estimate_tokens(
            ""
        )
        == 0
    )


def test_budget_fit():
    """
    Verify budget validation.
    """

    optimizer = TokenOptimizer()

    assert (
        optimizer.fits_budget(
            "hello world",
            100
        )
        is True
    )


def test_remaining_budget():
    """
    Verify remaining budget.
    """

    optimizer = TokenOptimizer()

    remaining = (
        optimizer.remaining_budget(
            "hello world",
            100
        )
    )

    assert remaining > 0
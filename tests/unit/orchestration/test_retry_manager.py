"""
File: tests/unit/orchestration/test_retry_manager.py

Purpose:
Unit tests for RetryManager.
"""

from core.orchestration.retry_manager import (
    RetryManager
)


def test_retry_manager_creation():
    """
    Verify initialization.
    """

    manager = RetryManager()

    assert manager is not None


def test_retry_allowed():
    """
    Verify retry allowed.
    """

    manager = RetryManager()

    assert (
        manager.should_retry(1)
        is True
    )


def test_retry_limit_reached():
    """
    Verify retry denied.
    """

    manager = RetryManager()

    assert (
        manager.should_retry(3)
        is False
    )


def test_custom_retry_limit():
    """
    Verify custom limit.
    """

    manager = RetryManager(
        max_retries=5
    )

    assert (
        manager.get_max_retries()
        == 5
    )


def test_retry_before_limit():
    """
    Verify retry below limit.
    """

    manager = RetryManager(
        max_retries=5
    )

    assert (
        manager.should_retry(4)
        is True
    )
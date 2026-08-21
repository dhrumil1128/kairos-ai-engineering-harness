"""
File: tests/unit/providers/test_provider_health.py

Purpose:
Unit tests for ProviderHealth.
"""

from core.providers.provider_health import (
    ProviderHealth
)


def test_health_creation():
    """
    Verify initialization.
    """

    health = ProviderHealth()

    assert health is not None


def test_set_healthy():
    """
    Verify healthy status.
    """

    health = ProviderHealth()

    health.set_status(
        "openai",
        True
    )

    assert (
        health.is_healthy(
            "openai"
        )
        is True
    )


def test_set_unhealthy():
    """
    Verify unhealthy status.
    """

    health = ProviderHealth()

    health.set_status(
        "claude",
        False
    )

    assert (
        health.is_healthy(
            "claude"
        )
        is False
    )


def test_healthy_count():
    """
    Verify healthy count.
    """

    health = ProviderHealth()

    health.set_status(
        "openai",
        True
    )

    health.set_status(
        "claude",
        True
    )

    health.set_status(
        "gemini",
        False
    )

    assert (
        health.healthy_count()
        == 2
    )


def test_total_providers():
    """
    Verify provider count.
    """

    health = ProviderHealth()

    health.set_status(
        "openai",
        True
    )

    health.set_status(
        "claude",
        False
    )

    assert (
        health.total_providers()
        == 2
    )
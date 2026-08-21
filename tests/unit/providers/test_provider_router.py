"""
File: tests/unit/providers/test_provider_router.py

Purpose:
Unit tests for ProviderRouter.
"""

from core.providers.provider_health import (
    ProviderHealth
)

from core.providers.provider_router import (
    ProviderRouter
)


def test_router_creation():
    """
    Verify initialization.
    """

    health = ProviderHealth()

    router = ProviderRouter(
        health
    )

    assert router is not None


def test_route_first_healthy():
    """
    Verify routing.
    """

    health = ProviderHealth()

    health.set_status(
        "openai",
        True
    )

    router = ProviderRouter(
        health
    )

    result = router.route(
        [
            "openai",
            "claude"
        ]
    )

    assert result == "openai"


def test_skip_unhealthy():
    """
    Verify fallback.
    """

    health = ProviderHealth()

    health.set_status(
        "openai",
        False
    )

    health.set_status(
        "claude",
        True
    )

    router = ProviderRouter(
        health
    )

    result = router.route(
        [
            "openai",
            "claude"
        ]
    )

    assert result == "claude"


def test_no_healthy_provider():
    """
    Verify no route.
    """

    health = ProviderHealth()

    health.set_status(
        "openai",
        False
    )

    health.set_status(
        "claude",
        False
    )

    router = ProviderRouter(
        health
    )

    result = router.route(
        [
            "openai",
            "claude"
        ]
    )

    assert result is None


def test_empty_provider_list():
    """
    Verify empty list.
    """

    health = ProviderHealth()

    router = ProviderRouter(
        health
    )

    result = router.route(
        []
    )

    assert result is None
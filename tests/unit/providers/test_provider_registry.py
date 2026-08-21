"""
File: tests/unit/providers/test_provider_registry.py

Purpose:
Unit tests for ProviderRegistry.
"""

from core.providers.provider_registry import (
    ProviderRegistry
)


def test_registry_creation():
    """
    Verify initialization.
    """

    registry = ProviderRegistry()

    assert registry is not None


def test_provider_registration():
    """
    Verify registration.
    """

    registry = ProviderRegistry()

    registry.register(
        "openai",
        object()
    )

    assert (
        registry.exists(
            "openai"
        )
        is True
    )


def test_provider_retrieval():
    """
    Verify retrieval.
    """

    registry = ProviderRegistry()

    provider = object()

    registry.register(
        "openai",
        provider
    )

    assert (
        registry.get(
            "openai"
        )
        == provider
    )


def test_provider_count():
    """
    Verify count.
    """

    registry = ProviderRegistry()

    registry.register(
        "openai",
        object()
    )

    registry.register(
        "claude",
        object()
    )

    assert (
        registry.count()
        == 2
    )


def test_missing_provider():
    """
    Verify missing lookup.
    """

    registry = ProviderRegistry()

    assert (
        registry.get(
            "missing"
        )
        is None
    )
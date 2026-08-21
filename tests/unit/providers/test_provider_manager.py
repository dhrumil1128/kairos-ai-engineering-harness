"""
File: tests/unit/providers/test_provider_manager.py

Purpose:
Unit tests for ProviderManager.
"""

from core.providers.provider_manager import (
    ProviderManager
)

from core.providers.provider_registry import (
    ProviderRegistry
)


def test_manager_creation():

    manager = (
        ProviderManager(
            ProviderRegistry()
        )
    )

    assert (
        manager is not None
    )


def test_register_provider():

    manager = (
        ProviderManager(
            ProviderRegistry()
        )
    )

    manager.register_provider(
        "gemini",
        object()
    )

    assert (
        manager.provider_exists(
            "gemini"
        )
    )


def test_provider_count():

    manager = (
        ProviderManager(
            ProviderRegistry()
        )
    )

    manager.register_provider(
        "gemini",
        object()
    )

    assert (
        manager.provider_count()
        == 1
    )


def test_get_provider():

    manager = (
        ProviderManager(
            ProviderRegistry()
        )
    )

    provider = object()

    manager.register_provider(
        "gemini",
        provider
    )

    assert (
        manager.get_provider(
            "gemini"
        )
        is provider
    )


def test_execute_exists():

    manager = (
        ProviderManager(
            ProviderRegistry()
        )
    )

    assert hasattr(
        manager,
        "execute"
    )
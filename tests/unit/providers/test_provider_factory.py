"""
File: tests/unit/providers/test_provider_factory.py

Purpose:
Unit tests for ProviderFactory.
"""

from core.providers.provider_factory import (
    ProviderFactory
)


def test_factory_creation():
    """
    Verify initialization.
    """

    factory = ProviderFactory()

    assert factory is not None


def test_openai_provider():
    """
    Verify OpenAI creation.
    """

    factory = ProviderFactory()

    provider = factory.create(
        "openai"
    )

    assert (
        provider["name"]
        == "openai"
    )


def test_claude_provider():
    """
    Verify Claude creation.
    """

    factory = ProviderFactory()

    provider = factory.create(
        "claude"
    )

    assert (
        provider["name"]
        == "claude"
    )


def test_unknown_provider():
    """
    Verify unknown handling.
    """

    factory = ProviderFactory()

    provider = factory.create(
        "unknown"
    )

    assert provider == {}


def test_supported_providers():
    """
    Verify provider list.
    """

    factory = ProviderFactory()

    providers = (
        factory.supported_providers()
    )

    assert (
        "openai"
        in providers
    )
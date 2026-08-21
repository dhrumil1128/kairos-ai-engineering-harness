"""
File: tests/unit/providers/test_anthropic_provider.py

Purpose:
Unit tests for AnthropicProvider.
"""

from core.providers.anthropic_provider import (
    AnthropicProvider
)


def test_provider_creation():
    """
    Verify initialization.
    """

    provider = (
        AnthropicProvider()
    )

    assert provider is not None


def test_provider_name():
    """
    Verify identity.
    """

    provider = (
        AnthropicProvider()
    )

    assert (
        provider.get_name()
        == "anthropic"
    )


def test_generate():
    """
    Verify response generation.
    """

    provider = (
        AnthropicProvider()
    )

    result = provider.generate(
        "hello"
    )

    assert (
        "Anthropic"
        in result
    )


def test_prompt_passthrough():
    """
    Verify prompt handling.
    """

    provider = (
        AnthropicProvider()
    )

    result = provider.generate(
        "test prompt"
    )

    assert (
        "test prompt"
        in result
    )


def test_supported_models():
    """
    Verify model list.
    """

    provider = (
        AnthropicProvider()
    )

    models = (
        provider.supported_models()
    )

    assert (
        "claude-sonnet"
        in models
    )
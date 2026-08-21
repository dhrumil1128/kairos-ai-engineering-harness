"""
File: tests/unit/providers/test_openai_provider.py

Purpose:
Unit tests for OpenAIProvider.
"""

from core.providers.openai_provider import (
    OpenAIProvider
)


def test_provider_creation():
    """
    Verify initialization.
    """

    provider = OpenAIProvider()

    assert provider is not None


def test_provider_name():
    """
    Verify identity.
    """

    provider = OpenAIProvider()

    assert (
        provider.get_name()
        == "openai"
    )


def test_generate():
    """
    Verify generation.
    """

    provider = OpenAIProvider()

    result = provider.generate(
        "hello"
    )

    assert (
        "OpenAI"
        in result
    )


def test_prompt_passthrough():
    """
    Verify prompt handling.
    """

    provider = OpenAIProvider()

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

    provider = OpenAIProvider()

    models = (
        provider.supported_models()
    )

    assert (
        "gpt-5"
        in models
    )
"""
File: tests/unit/providers/test_anthropic_sdk_client.py

Purpose:
Unit tests for AnthropicSDKClient.
"""

from core.providers.anthropic_sdk_client import (
    AnthropicSDKClient
)


def test_client_creation():
    """
    Verify initialization.
    """

    client = (
        AnthropicSDKClient()
    )

    assert client is not None


def test_generate():
    """
    Verify generation.
    """

    client = (
        AnthropicSDKClient()
    )

    result = client.generate(
        "hello"
    )

    assert (
        "Anthropic SDK"
        in result
    )


def test_prompt_passthrough():
    """
    Verify prompt handling.
    """

    client = (
        AnthropicSDKClient()
    )

    result = client.generate(
        "test prompt"
    )

    assert (
        "test prompt"
        in result
    )


def test_configured_true():
    """
    Verify configured state.
    """

    client = (
        AnthropicSDKClient(
            api_key="abc123"
        )
    )

    assert (
        client.configured()
        is True
    )


def test_configured_false():
    """
    Verify unconfigured state.
    """

    client = (
        AnthropicSDKClient()
    )

    assert (
        client.configured()
        is False
    )
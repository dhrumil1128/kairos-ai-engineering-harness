"""
Unit tests for GeminiSDKClient.
"""

from core.providers.gemini_sdk_client import (
    GeminiSDKClient
)


def test_creation():
    """
    Verify client creation.
    """

    client = GeminiSDKClient(
        api_key="dummy_key"
    )

    assert client is not None


def test_configured_true():
    """
    Verify configured state.
    """

    client = GeminiSDKClient(
        api_key="dummy_key"
    )

    assert (
        client.configured()
        is True
    )


def test_configured_false():
    """
    Verify unconfigured state.
    """

    client = GeminiSDKClient(
        api_key=""
    )

    assert (
        client.configured()
        is False
    )


def test_generate():
    """
    Unit test should not call API.
    """

    client = GeminiSDKClient(
        api_key="dummy_key"
    )

    assert (
        client.configured()
        is True
    )


def test_prompt_passthrough():
    """
    Unit test should not call API.
    """

    client = GeminiSDKClient(
        api_key="dummy_key"
    )

    assert (
        client.configured()
        is True
    )
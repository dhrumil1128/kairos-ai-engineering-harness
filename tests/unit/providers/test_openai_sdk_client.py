"""
File: tests/unit/providers/test_openai_sdk_client.py

Purpose:
Unit tests for OpenAISDKClient.
"""

from core.providers.openai_sdk_client import (
    OpenAISDKClient
)


def test_client_creation():
    client = OpenAISDKClient()

    assert client is not None


def test_generate():
    client = OpenAISDKClient()

    result = client.generate(
        "hello"
    )

    assert (
        "OpenAI SDK"
        in result
    )


def test_prompt_passthrough():
    client = OpenAISDKClient()

    result = client.generate(
        "test prompt"
    )

    assert (
        "test prompt"
        in result
    )


def test_configured_true():
    client = OpenAISDKClient(
        api_key="abc123"
    )

    assert (
        client.configured()
        is True
    )


def test_configured_false():
    client = OpenAISDKClient()

    assert (
        client.configured()
        is False
    )
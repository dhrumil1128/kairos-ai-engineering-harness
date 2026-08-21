"""
Unit tests for OllamaProvider.
"""

from unittest.mock import Mock

from core.providers.ollama_provider import (
    OllamaProvider
)

from core.providers.ollama_sdk_client import (
    OllamaSDKClient
)


def test_creation():

    client = Mock(
        spec=OllamaSDKClient
    )

    provider = OllamaProvider(
        client
    )

    assert provider is not None


def test_execute():

    client = Mock(
        spec=OllamaSDKClient
    )

    client.generate.return_value = (
        "hello"
    )

    provider = OllamaProvider(
        client
    )

    result = provider.execute(
        prompt="hello"
    )

    assert result == "hello"


def test_available():

    client = Mock(
        spec=OllamaSDKClient
    )

    client.health_check.return_value = (
        True
    )

    provider = OllamaProvider(
        client
    )

    assert (
        provider.available()
        is True
    )
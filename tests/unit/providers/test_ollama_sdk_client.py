"""
Unit tests for OllamaSDKClient.
"""

from unittest.mock import Mock
from unittest.mock import patch

from core.providers.ollama_sdk_client import (
    OllamaSDKClient
)


def test_creation():

    client = OllamaSDKClient()

    assert client is not None


@patch(
    "core.providers.ollama_sdk_client.requests.get"
)
def test_health_check_success(
    mock_get
):

    mock_response = Mock()

    mock_response.status_code = 200

    mock_get.return_value = mock_response

    client = OllamaSDKClient()

    assert (
        client.health_check()
        is True
    )


@patch(
    "core.providers.ollama_sdk_client.requests.post"
)
def test_generate(
    mock_post
):

    mock_response = Mock()

    mock_response.json.return_value = {
        "response": "Hello"
    }

    mock_response.raise_for_status = Mock()

    mock_post.return_value = mock_response

    client = OllamaSDKClient()

    result = client.generate(
        prompt="Hello"
    )

    assert result == "Hello"
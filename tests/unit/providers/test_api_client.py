"""
File: tests/unit/providers/test_api_client.py

Purpose:
Unit tests for APIClient.
"""

from core.providers.api_client import (
    APIClient
)


def test_client_creation():
    """
    Verify initialization.
    """

    client = APIClient()

    assert client is not None


def test_send_request():
    """
    Verify request sending.
    """

    client = APIClient()

    response = (
        client.send_request(
            "openai",
            "hello"
        )
    )

    assert (
        response["provider"]
        == "openai"
    )


def test_response_contains_prompt():
    """
    Verify prompt passthrough.
    """

    client = APIClient()

    response = (
        client.send_request(
            "openai",
            "test prompt"
        )
    )

    assert (
        response["prompt"]
        == "test prompt"
    )


def test_success_response():
    """
    Verify success status.
    """

    client = APIClient()

    response = (
        client.send_request(
            "openai",
            "hello"
        )
    )

    assert (
        client.is_successful(
            response
        )
        is True
    )


def test_failed_response():
    """
    Verify failure detection.
    """

    client = APIClient()

    assert (
        client.is_successful(
            {}
        )
        is False
    )
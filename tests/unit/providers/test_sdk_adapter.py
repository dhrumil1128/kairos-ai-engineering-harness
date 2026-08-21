"""
File: tests/unit/providers/test_sdk_adapter.py

Purpose:
Unit tests for SDKAdapter.
"""

from core.providers.sdk_adapter import (
    SDKAdapter
)


def test_adapter_creation():
    adapter = SDKAdapter()

    assert adapter is not None


def test_adapt_request():
    adapter = SDKAdapter()

    request = adapter.adapt_request(
        provider="openai",
        model="gpt-5",
        prompt="hello"
    )

    assert (
        request["provider"]
        == "openai"
    )


def test_request_validation():
    adapter = SDKAdapter()

    request = adapter.adapt_request(
        provider="anthropic",
        model="claude-sonnet",
        prompt="hello"
    )

    assert (
        adapter.is_valid(
            request
        )
        is True
    )


def test_adapt_response():
    adapter = SDKAdapter()

    response = adapter.adapt_response(
        provider="gemini",
        response="test"
    )

    assert (
        response["content"]
        == "test"
    )


def test_provider_preserved():
    adapter = SDKAdapter()

    response = adapter.adapt_response(
        provider="openai",
        response="hello"
    )

    assert (
        response["provider"]
        == "openai"
    )
"""
File: tests/unit/providers/test_real_provider_runtime.py

Purpose:
Unit tests for RealProviderRuntime.
"""

import pytest
import os 

from core.providers.real_provider_runtime import (
    RealProviderRuntime
)


class StubClient:
    def __init__(
        self,
        response
    ):
        self.response = response

    def generate(
        self,
        prompt: str,
        model: str
    ):
        return self.response


def test_runtime_creation():
    """
    Verify initialization.
    """

    runtime = (
        RealProviderRuntime()
    )

    assert runtime is not None


def test_provider_exists():
    """
    Verify provider lookup.
    """

    runtime = (
        RealProviderRuntime()
    )

    assert (
        runtime.provider_exists(
            "anthropic"
        )
        is True
    )


def test_openai_execution():
    """
    Verify OpenAI execution.
    """

    runtime = (
        RealProviderRuntime()
    )

    result = runtime.execute(
        provider="openai",
        prompt="hello",
        model="gpt-5"
    )

    assert (
        "OpenAI SDK"
        in result
    )

@pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY"),
    reason="GEMINI_API_KEY not configured"
)

def test_gemini_execution():
    """
    Verify Gemini execution.
    """

    runtime = (
        RealProviderRuntime()
    )

    result = runtime.execute(
    provider="gemini",
    prompt="Reply with KAIROS_TEST_OK",
    model="gemini-2.5-flash-lite"
)

    assert result is not None
    assert len(result) > 0


def test_unknown_provider():
    """
    Verify invalid provider.
    """

    runtime = (
        RealProviderRuntime()
    )

    with pytest.raises(
        ValueError
    ):
        runtime.execute(
            provider="unknown",
            prompt="hello",
            model="test"
        )


def test_structured_json_response_is_parsed():
    """
    Verify JSON strings are returned as Python objects.
    """

    runtime = (
        RealProviderRuntime()
    )

    runtime.providers["openai"] = StubClient(
        '{"name": "KAIROS", "version": "1.0"}'
    )

    result = runtime.execute(
        provider="openai",
        prompt="hello",
        model="gpt-5"
    )

    assert result == {
        "name": "KAIROS",
        "version": "1.0",
    }


def test_plain_text_response_falls_back_to_original():
    """
    Verify non-JSON text keeps existing response behavior.
    """

    runtime = (
        RealProviderRuntime()
    )

    runtime.providers["openai"] = StubClient(
        "OpenAI SDK response: hello"
    )

    result = runtime.execute(
        provider="openai",
        prompt="hello",
        model="gpt-5"
    )

    assert result == "OpenAI SDK response: hello"


def test_structured_python_response_is_not_parsed_again():
    """
    Verify provider-native structured objects pass through unchanged.
    """

    runtime = (
        RealProviderRuntime()
    )

    response = {
        "name": "KAIROS"
    }

    runtime.providers["openai"] = StubClient(
        response
    )

    result = runtime.execute(
        provider="openai",
        prompt="hello",
        model="gpt-5"
    )

    assert result is response

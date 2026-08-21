"""
File: tests/unit/providers/test_provider_runtime.py

Purpose:
Unit tests for ProviderRuntime.
"""

from core.providers.api_client import (
    APIClient
)

from core.providers.response_parser import (
    ResponseParser
)

from core.providers.provider_executor import (
    ProviderExecutor
)

from core.providers.provider_runtime import (
    ProviderRuntime
)

from core.providers.request_builder import (
    RequestBuilder
)


def create_runtime():
    executor = ProviderExecutor(
        APIClient(),
        ResponseParser()
    )

    builder = RequestBuilder()

    return ProviderRuntime(
        executor,
        builder
    )


def test_runtime_creation():
    runtime = create_runtime()

    assert runtime is not None


def test_runtime_execution():
    runtime = create_runtime()

    result = runtime.run(
        provider="openai",
        model="gpt-5",
        prompt="hello"
    )

    assert (
        result["success"]
        is True
    )


def test_provider_preserved():
    runtime = create_runtime()

    result = runtime.run(
        provider="anthropic",
        model="claude-sonnet",
        prompt="hello"
    )

    assert (
        result["provider"]
        == "anthropic"
    )


def test_content_returned():
    runtime = create_runtime()

    result = runtime.run(
        provider="gemini",
        model="gemini-pro",
        prompt="test"
    )

    assert (
        "Response"
        in result["content"]
    )


def test_multiple_runs():
    runtime = create_runtime()

    result = runtime.run(
        provider="openai",
        model="gpt-5",
        prompt="build api"
    )

    assert (
        result["success"]
        is True
    )
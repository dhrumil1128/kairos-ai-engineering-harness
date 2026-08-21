"""
File: tests/unit/providers/test_provider_executor.py

Purpose:
Unit tests for ProviderExecutor.
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


def test_executor_creation():
    """
    Verify initialization.
    """

    executor = ProviderExecutor(
        APIClient(),
        ResponseParser()
    )

    assert executor is not None


def test_execute_request():
    """
    Verify execution.
    """

    executor = ProviderExecutor(
        APIClient(),
        ResponseParser()
    )

    result = executor.execute(
        "openai",
        "hello"
    )

    assert (
        result["success"]
        is True
    )


def test_provider_preserved():
    """
    Verify provider value.
    """

    executor = ProviderExecutor(
        APIClient(),
        ResponseParser()
    )

    result = executor.execute(
        "anthropic",
        "hello"
    )

    assert (
        result["provider"]
        == "anthropic"
    )


def test_content_returned():
    """
    Verify content extraction.
    """

    executor = ProviderExecutor(
        APIClient(),
        ResponseParser()
    )

    result = executor.execute(
        "gemini",
        "test"
    )

    assert (
        "Response"
        in result["content"]
    )


def test_prompt_execution():
    """
    Verify prompt execution.
    """

    executor = ProviderExecutor(
        APIClient(),
        ResponseParser()
    )

    result = executor.execute(
        "openai",
        "build api"
    )

    assert (
        result["success"]
        is True
    )
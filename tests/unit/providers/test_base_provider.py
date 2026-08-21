"""
File: tests/unit/providers/test_base_provider.py

Purpose:
Unit tests for BaseProvider.
"""

from core.providers.base_provider import (
    BaseProvider
)


class MockProvider(
    BaseProvider
):
    """
    Mock provider for testing.
    """

    def __init__(self):
        super().__init__(
            "mock"
        )

    def generate(
        self,
        prompt: str
    ) -> str:
        return (
            f"Generated: {prompt}"
        )


def test_provider_creation():
    """
    Verify initialization.
    """

    provider = MockProvider()

    assert provider is not None


def test_provider_name():
    """
    Verify provider identity.
    """

    provider = MockProvider()

    assert (
        provider.get_name()
        == "mock"
    )


def test_generate():
    """
    Verify generation.
    """

    provider = MockProvider()

    result = provider.generate(
        "hello"
    )

    assert (
        "Generated"
        in result
    )


def test_prompt_passthrough():
    """
    Verify prompt handling.
    """

    provider = MockProvider()

    result = provider.generate(
        "test prompt"
    )

    assert (
        "test prompt"
        in result
    )


def test_multiple_calls():
    """
    Verify repeat calls.
    """

    provider = MockProvider()

    assert (
        provider.generate("A")
        != ""
    )
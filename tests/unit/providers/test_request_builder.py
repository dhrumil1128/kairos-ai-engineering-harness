"""
File: tests/unit/providers/test_request_builder.py

Purpose:
Unit tests for RequestBuilder.
"""

from core.providers.request_builder import (
    RequestBuilder
)


def test_builder_creation():
    builder = RequestBuilder()

    assert builder is not None


def test_build_request():
    builder = RequestBuilder()

    request = builder.build(
        prompt="hello",
        provider="openai",
        model="gpt-5"
    )

    assert (
        request["provider"]
        == "openai"
    )


def test_prompt_preserved():
    builder = RequestBuilder()

    request = builder.build(
        prompt="build api",
        provider="openai",
        model="gpt-5"
    )

    assert (
        request["prompt"]
        == "build api"
    )


def test_model_preserved():
    builder = RequestBuilder()

    request = builder.build(
        prompt="hello",
        provider="anthropic",
        model="claude-sonnet"
    )

    assert (
        request["model"]
        == "claude-sonnet"
    )


def test_validate_request():
    builder = RequestBuilder()

    request = builder.build(
        prompt="hello",
        provider="openai",
        model="gpt-5"
    )

    assert (
        builder.validate(
            request
        )
        is True
    )
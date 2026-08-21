"""
File: tests/unit/providers/test_model_router.py

Purpose:
Unit tests for ModelRouter.
"""

from core.providers.model_router import (
    ModelRouter
)


def test_router_creation():
    """
    Verify router creation.
    """

    router = (
        ModelRouter()
    )

    assert (
        router is not None
    )


def test_route_returns_dict():
    """
    Verify route returns dict.
    """

    router = (
        ModelRouter()
    )

    result = (
        router.route(
            "coding",
            "gemini"
        )
    )

    assert isinstance(
        result,
        dict
    )


def test_route_contains_provider():
    """
    Verify provider exists.
    """

    router = (
        ModelRouter()
    )

    result = (
        router.route(
            "coding",
            "gemini"
        )
    )

    assert (
        "provider"
        in result
    )


def test_route_contains_model():
    """
    Verify model exists.
    """

    router = (
        ModelRouter()
    )

    result = (
        router.route(
            "coding",
            "gemini"
        )
    )

    assert (
        "model"
        in result
    )


def test_gemini_coding_route():
    """
    Verify Gemini route.
    """

    router = (
        ModelRouter()
    )

    result = (
        router.route(
            "coding",
            "gemini"
        )
    )

    assert (
        result["provider"]
        == "gemini"
    )


def test_anthropic_coding_route():
    """
    Verify Anthropic route.
    """

    router = (
        ModelRouter()
    )

    result = (
        router.route(
            "coding",
            "anthropic"
        )
    )

    assert (
        result["provider"]
        == "anthropic"
    )


def test_openai_coding_route():
    """
    Verify OpenAI route.
    """

    router = (
        ModelRouter()
    )

    result = (
        router.route(
            "coding",
            "openai"
        )
    )

    assert (
        result["provider"]
        == "openai"
    )


def test_unknown_provider():
    """
    Verify fallback route.
    """

    router = (
        ModelRouter()
    )

    result = (
        router.route(
            "coding",
            "unknown"
        )
    )

    assert (
        result["provider"]
        == "unknown"
    )
"""
File: tests/unit/llm/test_model_router.py

Purpose:
Unit tests for ModelRouter.

Why:
Verify model selection and route management.

Architecture:

Task
    ↓
Model Router
    ↓
Selected Model
"""

# Model routing layer under test.
from core.llm.model_router import (
    ModelRouter
)


def test_model_router_creation():
    """
    Verify router initialization.
    """

    router = ModelRouter()

    assert router is not None


def test_summary_route():
    """
    Verify summary task routing.
    """

    router = ModelRouter()

    model = router.get_model(
        "summary"
    )

    assert model == "gemini-flash"


def test_coding_route():
    """
    Verify coding task routing.
    """

    router = ModelRouter()

    model = router.get_model(
        "coding"
    )

    assert model == "gpt-5"


def test_add_route():
    """
    Verify custom route creation.
    """

    router = ModelRouter()

    router.add_route(
        "research",
        "claude-opus"
    )

    assert (
        router.get_model("research")
        == "claude-opus"
    )


def test_default_route():
    """
    Verify fallback model selection.
    """

    router = ModelRouter()

    model = router.get_model(
        "unknown_task"
    )

    assert model == "gpt-5"


def test_route_count():
    """
    Verify route counting.
    """

    router = ModelRouter()

    assert router.count() == 4
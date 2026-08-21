"""
File: tests/unit/llm/test_provider_manager.py

Purpose:
Unit tests for ProviderManager.

Why:
Verify provider registration,
retrieval, existence checks,
and counting.

Architecture:

Agents
    ↓
Provider Manager
    ↓
Provider Registry
"""

# LLM provider layer under test.
from core.llm.provider_manager import (
    ProviderManager
)


def test_provider_manager_creation():
    """
    Verify manager initialization.
    """

    manager = ProviderManager()

    assert manager is not None


def test_register_provider():
    """
    Verify provider registration.
    """

    manager = ProviderManager()

    manager.register_provider(
        "openai",
        {
            "model": "gpt-5"
        }
    )

    assert manager.count() == 1


def test_get_provider():
    """
    Verify provider retrieval.
    """

    manager = ProviderManager()

    manager.register_provider(
        "openai",
        {
            "model": "gpt-5"
        }
    )

    provider = manager.get_provider(
        "openai"
    )

    assert provider["model"] == "gpt-5"


def test_provider_exists():
    """
    Verify existence checks.
    """

    manager = ProviderManager()

    manager.register_provider(
        "anthropic",
        {
            "model": "claude-opus"
        }
    )

    assert manager.exists(
        "anthropic"
    ) is True

    assert manager.exists(
        "openai"
    ) is False


def test_provider_count():
    """
    Verify provider counting.
    """

    manager = ProviderManager()

    manager.register_provider(
        "openai",
        {
            "model": "gpt-5"
        }
    )

    manager.register_provider(
        "anthropic",
        {
            "model": "claude-opus"
        }
    )

    assert manager.count() == 2
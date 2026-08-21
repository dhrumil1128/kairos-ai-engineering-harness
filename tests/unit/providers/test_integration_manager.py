"""
File: tests/unit/providers/test_integration_manager.py

Purpose:
Unit tests for IntegrationManager.
"""

from core.providers.integration_manager import (
    IntegrationManager
)

from core.providers.real_provider_runtime import (
    RealProviderRuntime
)


def create_manager():
    runtime = RealProviderRuntime()

    return IntegrationManager(
        runtime
    )


def test_manager_creation():
    """
    Verify initialization.
    """

    manager = create_manager()

    assert manager is not None


def test_provider_available():
    """
    Verify provider lookup.
    """

    manager = create_manager()

    assert (
        manager.provider_available(
            "openai"
        )
        is True
    )


def test_provider_missing():
    """
    Verify invalid provider.
    """

    manager = create_manager()

    assert (
        manager.provider_available(
            "unknown"
        )
        is False
    )


def test_execute_openai():
    """
    Verify OpenAI execution.
    """

    manager = create_manager()

    result = manager.execute(
        provider="openai",
        prompt="hello",
        model="gpt-5"
    )

    assert (
        "OpenAI SDK"
        in result
    )


def test_execute_anthropic():
    """
    Verify Anthropic execution.
    """

    manager = create_manager()

    result = manager.execute(
        provider="anthropic",
        prompt="hello",
        model="claude-sonnet"
    )

    assert (
        "Anthropic SDK"
        in result
    )
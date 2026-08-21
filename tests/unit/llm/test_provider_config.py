"""
File: tests/unit/llm/test_provider_config.py

Purpose:
Unit tests for ProviderConfig.

Why:
Verify provider configuration loading.

Architecture:

providers.yaml
        ↓
ProviderConfig
        ↓
ProviderManager
"""

# Provider configuration loader.
from core.llm.provider_config import (
    ProviderConfig
)


def test_provider_config_creation():
    """
    Verify config loader initialization.
    """

    config = ProviderConfig(
        "config/providers.yaml"
    )

    assert config is not None


def test_load_configuration():
    """
    Verify configuration loading.
    """

    config = ProviderConfig(
        "config/providers.yaml"
    )

    data = config.load()

    assert data is not None


def test_providers_section_exists():
    """
    Verify providers section exists.
    """

    config = ProviderConfig(
        "config/providers.yaml"
    )

    data = config.load()

    assert "providers" in data


def test_routing_section_exists():
    """
    Verify routing section exists.
    """

    config = ProviderConfig(
        "config/providers.yaml"
    )

    data = config.load()

    assert "routing" in data


def test_failover_section_exists():
    """
    Verify failover section exists.
    """

    config = ProviderConfig(
        "config/providers.yaml"
    )

    data = config.load()

    assert "failover" in data
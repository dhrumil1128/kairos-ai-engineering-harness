"""
File: tests/unit/providers/test_provider_config.py

Purpose:
Unit tests for ProviderConfig.
"""

from pathlib import Path

import yaml

from core.providers.provider_config import (
    ProviderConfig
)


def test_config_creation():
    """
    Verify initialization.
    """

    config = ProviderConfig()

    assert config is not None


def test_missing_config():
    """
    Verify missing config.
    """

    config = ProviderConfig(
        "missing.yaml"
    )

    assert (
        config.load()
        == {}
    )


def test_config_exists():
    """
    Verify existence.
    """

    file_path = Path(
        "temp_config.yaml"
    )

    file_path.write_text(
        "providers: {}",
        encoding="utf-8"
    )

    config = ProviderConfig(
        "temp_config.yaml"
    )

    assert (
        config.exists()
        is True
    )

    file_path.unlink()


def test_load_config():
    """
    Verify loading.
    """

    file_path = Path(
        "temp_config.yaml"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        yaml.safe_dump(
            {
                "providers": {
                    "openai": {}
                }
            },
            file
        )

    config = ProviderConfig(
        "temp_config.yaml"
    )

    result = config.load()

    assert (
        "providers"
        in result
    )

    file_path.unlink()


def test_missing_exists():
    """
    Verify missing file.
    """

    config = ProviderConfig(
        "unknown.yaml"
    )

    assert (
        config.exists()
        is False
    )
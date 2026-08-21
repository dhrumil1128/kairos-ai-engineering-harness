"""
File: tests/unit/providers/test_credential_manager.py

Purpose:
Unit tests for CredentialManager.
"""

from pathlib import Path

import yaml

from core.providers.provider_config import (
    ProviderConfig
)

from core.providers.credential_manager import (
    CredentialManager
)


def create_temp_config():
    """
    Create temporary config.
    """

    path = Path(
        "temp_providers.yaml"
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        yaml.safe_dump(
            {
                "providers": {
                    "openai": {
                        "api_key": "abc123"
                    }
                }
            },
            file
        )

    return path


def test_manager_creation():
    """
    Verify initialization.
    """

    config = ProviderConfig()

    manager = CredentialManager(
        config
    )

    assert manager is not None


def test_get_api_key():
    """
    Verify API key retrieval.
    """

    path = create_temp_config()

    config = ProviderConfig(
        str(path)
    )

    manager = CredentialManager(
        config
    )

    assert (
        manager.get_api_key(
            "openai"
        )
        == "abc123"
    )

    path.unlink()


def test_has_api_key():
    """
    Verify API key existence.
    """

    path = create_temp_config()

    config = ProviderConfig(
        str(path)
    )

    manager = CredentialManager(
        config
    )

    assert (
        manager.has_api_key(
            "openai"
        )
        is True
    )

    path.unlink()


def test_missing_provider():
    """
    Verify missing provider.
    """

    path = create_temp_config()

    config = ProviderConfig(
        str(path)
    )

    manager = CredentialManager(
        config
    )

    assert (
        manager.get_api_key(
            "gemini"
        )
        == ""
    )

    path.unlink()


def test_missing_key():
    """
    Verify missing key.
    """

    config = ProviderConfig(
        "missing.yaml"
    )

    manager = CredentialManager(
        config
    )

    assert (
        manager.has_api_key(
            "openai"
        )
        is False
    )
"""
File: tests/unit/providers/test_integration_config.py
"""

from pathlib import Path

import yaml

from core.providers.provider_config import (
    ProviderConfig
)

from core.providers.credential_manager import (
    CredentialManager
)

from core.providers.integration_config import (
    IntegrationConfig
)


def create_config():
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
                    "gemini": {
                        "api_key": "abc123"
                    }
                }
            },
            file
        )

    return path


def test_creation():
    path = create_config()

    config = ProviderConfig(
        str(path)
    )

    credentials = CredentialManager(
        config
    )

    integration = IntegrationConfig(
        credentials
    )

    assert integration is not None

    path.unlink()


def test_can_run():
    path = create_config()

    config = ProviderConfig(
        str(path)
    )

    credentials = CredentialManager(
        config
    )

    integration = IntegrationConfig(
        credentials
    )

    assert (
        integration.can_run(
            "gemini"
        )
        is True
    )

    path.unlink()


def test_missing_provider():
    path = create_config()

    config = ProviderConfig(
        str(path)
    )

    credentials = CredentialManager(
        config
    )

    integration = IntegrationConfig(
        credentials
    )

    assert (
        integration.can_run(
            "openai"
        )
        is False
    )

    path.unlink()


def test_missing_file():
    config = ProviderConfig(
        "missing.yaml"
    )

    credentials = CredentialManager(
        config
    )

    integration = IntegrationConfig(
        credentials
    )

    assert (
        integration.can_run(
            "gemini"
        )
        is False
    )


def test_multiple_checks():
    path = create_config()

    config = ProviderConfig(
        str(path)
    )

    credentials = CredentialManager(
        config
    )

    integration = IntegrationConfig(
        credentials
    )

    assert integration.can_run(
        "gemini"
    )

    path.unlink()
"""
File: core/providers/credential_manager.py

Purpose:
Manage provider credentials.

Why:

KAIROS should access provider
credentials through a central
manager instead of directly
reading configuration files.

Future:

V2:
- Environment variables

V3:
- Secret managers

V4:
- Key rotation

V5:
- Enterprise vault support
"""

from core.providers.provider_config import (
    ProviderConfig
)


class CredentialManager:
    """
    Manage provider credentials.
    """

    def __init__(
        self,
        config: ProviderConfig
    ):
        """
        Initialize manager.
        """

        self.config = config

    def get_api_key(
        self,
        provider_name: str
    ) -> str:
        """
        Return API key.

        Parameters:
            provider_name:
                Provider identifier.

        Returns:
            API key or empty string.
        """

        data = self.config.load()

        providers = data.get(
            "providers",
            {}
        )

        provider = providers.get(
            provider_name,
            {}
        )

        return provider.get(
            "api_key",
            ""
        )

    def has_api_key(
        self,
        provider_name: str
    ) -> bool:
        """
        Check if API key exists.
        """

        return bool(
            self.get_api_key(
                provider_name
            )
        )
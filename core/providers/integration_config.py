"""
File: core/providers/integration_config.py

Purpose:
Manage integration test settings.

Why:

Integration tests should only
run when provider credentials
are available.
"""

from core.providers.credential_manager import (
    CredentialManager
)


class IntegrationConfig:
    """
    Integration configuration.
    """

    def __init__(
        self,
        credentials: CredentialManager
    ):
        self.credentials = credentials

    def can_run(
        self,
        provider: str
    ) -> bool:
        """
        Check if integration test
        can run.
        """

        return self.credentials.has_api_key(
            provider
        )
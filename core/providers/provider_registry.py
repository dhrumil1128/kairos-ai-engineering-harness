"""
File: core/providers/provider_registry.py

Purpose:
Register and manage available
LLM providers.

Why:

KAIROS supports multiple
providers and needs a central
registry.

Future:

V2:
- Dynamic registration

V3:
- Provider capabilities

V4:
- Health integration

V5:
- Auto-discovery
"""


class ProviderRegistry:
    """
    Manage provider registrations.
    """

    def __init__(self):
        """
        Initialize registry.
        """

        self.providers = {}

    def register(
        self,
        name: str,
        provider: object
    ) -> None:
        """
        Register provider.
        """

        self.providers[name] = provider

    def get(
        self,
        name: str
    ) -> object | None:
        """
        Retrieve provider.
        """

        return self.providers.get(
            name
        )

    def exists(
        self,
        name: str
    ) -> bool:
        """
        Check provider existence.
        """

        return name in self.providers

    def count(
        self
    ) -> int:
        """
        Return provider count.
        """

        return len(
            self.providers
        )
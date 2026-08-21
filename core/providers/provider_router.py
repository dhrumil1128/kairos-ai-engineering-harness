"""
File: core/providers/provider_router.py

Purpose:
Route requests to the most
appropriate provider.

Why:

Enterprise systems should not
hardcode a single provider.

Future:

V2:
- Cost-based routing

V3:
- Latency-based routing

V4:
- Capability-based routing

V5:
- Dynamic optimization
"""

from core.providers.provider_health import (
    ProviderHealth
)


class ProviderRouter:
    """
    Route provider requests.
    """

    def __init__(
        self,
        health: ProviderHealth
    ):
        """
        Initialize router.
        """

        self.health = health

    def route(
        self,
        providers: list[str]
    ) -> str | None:
        """
        Select first healthy provider.

        Parameters:
            providers:
                Candidate providers.

        Returns:
            Selected provider.
        """

        for provider in providers:

            if self.health.is_healthy(
                provider
            ):
                return provider

        return None
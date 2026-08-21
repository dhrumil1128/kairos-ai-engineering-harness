"""
File: core/providers/integration_manager.py

Purpose:
Manage provider integrations.

Why:

Provides a central point for
executing provider requests
through the real provider runtime.

Future:

V2:
- Real API execution

V3:
- Health checks

V4:
- Failover routing

V5:
- Multi-provider orchestration
"""

from core.providers.real_provider_runtime import (
    RealProviderRuntime
)


class IntegrationManager:
    """
    Manage provider integrations.
    """

    def __init__(
        self,
        runtime: RealProviderRuntime
    ):
        """
        Initialize manager.
        """

        self.runtime = runtime

    def execute(
        self,
        provider: str,
        prompt: str,
        model: str
    ) -> str:
        """
        Execute request.
        """

        return self.runtime.execute(
            provider=provider,
            prompt=prompt,
            model=model
        )

    def provider_available(
        self,
        provider: str
    ) -> bool:
        """
        Check provider availability.
        """

        return self.runtime.provider_exists(
            provider
        )
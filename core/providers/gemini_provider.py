"""
File: core/providers/gemini_provider.py

Purpose:
Gemini provider implementation.

Why:

Provides a concrete implementation
of the BaseProvider interface.

Future:

V2:
- Streaming support

V3:
- Tool calling

V4:
- Multi-modal

V5:
- Advanced agent workflows
"""

from core.providers.base_provider import (
    BaseProvider
)

from core.providers.gemini_sdk_client import (
    GeminiSDKClient
)


class GeminiProvider(
    BaseProvider
):
    """
    Gemini provider.
    """

    def __init__(
        self
    ):
        """
        Initialize provider.
        """

        super().__init__(
            "gemini"
        )

        self.client = (
            GeminiSDKClient()
        )

    def generate(
        self,
        prompt: str,
        model: str = (
            "gemini-2.5-flash-lite"
        )
    ) -> str:
        """
        Generate response.
        """

        return (
            self.client.generate(
                prompt=prompt,
                model=model
            )
        )

    def configured(
        self
    ) -> bool:
        """
        Check configuration.
        """

        return (
            self.client.configured()
        )

    def supported_models(
        self
    ) -> list[str]:
        """
        Return supported models.
        """

        return [
            "gemini-2.5-pro",
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
        ]
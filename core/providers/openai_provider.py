"""
File: core/providers/openai_provider.py

Purpose:
OpenAI provider implementation.

Why:

Provides a concrete implementation
of the BaseProvider interface.

Future:

V2:
- Real OpenAI SDK

V3:
- Streaming support

V4:
- Function calling

V5:
- Advanced agent workflows
"""

from core.providers.base_provider import (
    BaseProvider
)


class OpenAIProvider(
    BaseProvider
):
    """
    OpenAI provider.
    """

    def __init__(self):
        """
        Initialize provider.
        """

        super().__init__(
            "openai"
        )

    def generate(
        self,
        prompt: str
    ) -> str:
        """
        Generate response.

        Parameters:
            prompt:
                User prompt.

        Returns:
            Provider response.
        """

        return (
            f"OpenAI response: {prompt}"
        )

    def supported_models(
        self
    ) -> list[str]:
        """
        Return supported models.
        """

        return [
            "gpt-5",
            "gpt-5-mini",
            "gpt-5-nano",
            "gpt-4.1",
        ]
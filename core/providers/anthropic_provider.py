"""
File: core/providers/anthropic_provider.py

Purpose:
Anthropic provider implementation.

Why:

Provides a concrete implementation
of the BaseProvider interface.

Future:

V2:
- Real Anthropic SDK

V3:
- Streaming support

V4:
- Tool use

V5:
- Advanced agent workflows
"""

from core.providers.base_provider import (
    BaseProvider
)


class AnthropicProvider(
    BaseProvider
):
    """
    Anthropic provider.
    """

    def __init__(self):
        """
        Initialize provider.
        """

        super().__init__(
            "anthropic"
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
            f"Anthropic response: {prompt}"
        )

    def supported_models(
        self
    ) -> list[str]:
        """
        Return supported models.
        """

        return [
            "claude-opus",
            "claude-sonnet",
            "claude-haiku",
        ]
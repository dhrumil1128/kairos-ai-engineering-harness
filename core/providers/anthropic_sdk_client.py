"""
File: core/providers/anthropic_sdk_client.py

Purpose:
Anthropic SDK client wrapper.

Why:

Encapsulates all Anthropic SDK
interactions behind a simple
interface.

Future:

V2:
- Real Anthropic SDK

V3:
- Streaming

V4:
- Tool Use

V5:
- Multi-modal support
"""


class AnthropicSDKClient:
    """
    Anthropic SDK wrapper.
    """

    def __init__(
        self,
        api_key: str = ""
    ):
        """
        Initialize client.
        """

        self.api_key = api_key

    def generate(
        self,
        prompt: str,
        model: str = (
            "claude-sonnet"
        )
    ) -> str:
        """
        Generate response.
        """

        return (
            f"Anthropic SDK response: {prompt}"
        )

    def configured(
        self
    ) -> bool:
        """
        Check configuration.
        """

        return bool(
            self.api_key
        )
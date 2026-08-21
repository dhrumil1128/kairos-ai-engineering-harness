"""
File: core/providers/openai_sdk_client.py

Purpose:
OpenAI SDK client wrapper.

Why:

Encapsulates all OpenAI SDK
interactions behind a simple
interface.

Future:

V2:
- Real OpenAI SDK

V3:
- Streaming

V4:
- Function Calling

V5:
- Multi-modal support
"""


class OpenAISDKClient:
    """
    OpenAI SDK wrapper.
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
        model: str = "gpt-5"
    ) -> str:
        """
        Generate response.
        """

        return (
            f"OpenAI SDK response: {prompt}"
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
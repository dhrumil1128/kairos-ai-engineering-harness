"""
File: core/providers/nvidia_provider.py

Purpose:
NVIDIA provider implementation.
"""

from core.providers.base_provider import (
    BaseProvider
)

from core.providers.nvidia_sdk_client import (
    NvidiaSDKClient
)


class NvidiaProvider(
    BaseProvider
):
    """
    NVIDIA provider.
    """

    def __init__(
        self
    ):
        """
        Initialize provider.
        """

        super().__init__(
            "nvidia"
        )

        self.client = (
            NvidiaSDKClient()
        )

    def generate(
        self,
        prompt: str
    ) -> str:
        """
        Generate response.
        """

        return (
            self.client.generate(
                prompt
            )
        )

    def supported_models(
        self
    ) -> list[str]:
        """
        Return supported models.
        """

        return [
            "meta/llama-3.3-70b-instruct",
            "meta/llama-3.1-70b-instruct",
            "qwen/qwen3.5-122b-a10b",
            "deepseek-ai/deepseek-v4-pro",
            "moonshotai/kimi-k2.6",
            "z-ai/glm-5.2",
            "google/gemma-4-31b-it",
            "google/gemma-3-4b-it"
        ]

    def configured(
        self
    ) -> bool:
        """
        Check provider configuration.
        """

        return (
            self.client
            .configured()
        )
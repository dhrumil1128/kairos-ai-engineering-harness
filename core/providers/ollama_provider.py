"""
File: core/providers/ollama_provider.py

Purpose:
Provider wrapper for Ollama.
"""

from core.providers.ollama_sdk_client import (
    OllamaSDKClient
)


class OllamaProvider:
    """
    Ollama provider.
    """

    def __init__(
        self,
        client: OllamaSDKClient
    ):
        self.client = client

    def execute(
        self,
        prompt: str,
        model: str = "qwen3:8b"
    ) -> str:
        """
        Execute request.
        """

        return self.client.generate(
            prompt=prompt,
            model=model
        )

    def available(
        self
    ) -> bool:
        """
        Check availability.
        """

        return self.client.health_check()
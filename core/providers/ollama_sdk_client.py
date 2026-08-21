"""
File: core/providers/ollama_sdk_client.py

Purpose:
Ollama SDK client.

Provides local model execution
through Ollama.
"""

import requests

from core.logging.kairos_logger import (
    KairosLogger
)


class OllamaSDKClient:

    """
    Ollama SDK wrapper.
    """

    def __init__(
        self,
        host: str = "http://localhost:11434"
    ):
        self.host = host
        
        # KAIROS logger.
        self.logger = KairosLogger(
            "kairos"
        )

    def generate(
        self,
        prompt: str,
        model: str = "qwen3:8b"
    ) -> str:
        """
        Generate response.
        """
        
        self.logger.debug(
    f"Ollama Model={model}"
        )

        self.logger.debug(
            f"Prompt Length={len(prompt)}"
        )

        self.logger.debug(
            "Request started"
        )

        response = requests.post(
            f"{self.host}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=600
        )


        response.raise_for_status()
        self.logger.debug(
    "Response received"
)

        data = response.json()

        return data.get(
            "response",
            ""
        )

    def health_check(
        self
    ) -> bool:
        """
        Verify Ollama availability.
        """

        try:

            response = requests.get(
                f"{self.host}/api/tags",
                timeout=10
            )

            return (
                response.status_code == 200
            )

        except Exception:
            return False
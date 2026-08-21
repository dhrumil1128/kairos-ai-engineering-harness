"""
File: core/providers/gemini_sdk_client.py

Purpose:
Gemini SDK client wrapper.

Why:

Encapsulates all Gemini SDK
interactions behind a simple
interface.

Future:

V2:
- Real Gemini SDK

V3:
- Streaming

V4:
- Tool Calling

V5:
- Multi-modal support
"""


import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiSDKClient:
    """
    Gemini SDK wrapper.
    """

    def __init__(
        self,
        api_key: str = ""
    ):
        """
        Initialize client.
        """

        self.api_key = (
            api_key
            or os.getenv(
                "GEMINI_API_KEY",
                ""
            )
        )

    def generate(
        self,
        prompt: str,
        # Fallback model.
        # Normally ModelRouter
        # provides the model.
        model: str = (
            "gemini-2.5-flash-lite"
        )
    ) -> str:
        """
        Generate real Gemini response.
        """

        if not self.api_key:
            raise ValueError(
                "Gemini API key not configured."
            )

        client = genai.Client(
            api_key=self.api_key
        )

        response = (
            client.models.generate_content(
                model=model,
                contents=prompt
            )
        )

        return response.text

    def configured(
        self
    ) -> bool:
        """
        Check configuration.
        """

        return bool(
            self.api_key
        )
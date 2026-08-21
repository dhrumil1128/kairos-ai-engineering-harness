"""
File: core/providers/base_provider.py

Purpose:
Base interface for all LLM
providers.

Why:

Every provider should expose
a consistent interface to the
rest of KAIROS.

Architecture:

BaseProvider
      ↓

OpenAIProvider
AnthropicProvider
GeminiProvider
GroqProvider
OllamaProvider

Future:

V2:
- Streaming support

V3:
- Tool calling

V4:
- Structured outputs

V5:
- Agent-native execution
"""

from abc import ABC
from abc import abstractmethod


class BaseProvider(ABC):
    """
    Base provider interface.
    """

    def __init__(
        self,
        provider_name: str
    ):
        """
        Initialize provider.
        """

        self.provider_name = (
            provider_name
        )

    @abstractmethod
    def generate(
        self,
        prompt: str
    ) -> str:
        """
        Generate response.

        Must be implemented
        by child providers.
        """

    def get_name(
        self
    ) -> str:
        """
        Return provider name.
        """

        return self.provider_name
"""
File: core/llm/provider_manager.py

Purpose:
Manage LLM providers across KAIROS.

Why:

KAIROS must support multiple providers:

- OpenAI
- Anthropic
- Google
- Groq
- Ollama
- Future Providers

Agents should never directly interact
with provider-specific implementations.

Architecture:

Agents
    ↓
Provider Manager
    ↓
Provider Registry
    ↓
Selected Model

Version 1:

Provider registration and retrieval.

Future Versions:

V2:
- API key management

V3:
- Health checks

V4:
- Automatic failover

V5:
- Cost-aware routing
"""

# Structured typing.
from typing import Dict, Any


class ProviderManager:
    """
    Central provider registry.

    Stores and manages available
    LLM providers.
    """

    def __init__(self):
        """
        Initialize provider registry.
        """

        self.providers: Dict[
            str,
            Dict[str, Any]
        ] = {}

    def register_provider(
        self,
        name: str,
        config: Dict[str, Any]
    ) -> None:
        """
        Register a provider.

        Example:

        register_provider(
            "openai",
            {
                "model": "gpt-5",
                "api_key": "..."
            }
        )
        """

        self.providers[name] = config

    def get_provider(
        self,
        name: str
    ) -> Dict[str, Any] | None:
        """
        Retrieve provider configuration.
        """

        return self.providers.get(name)

    def exists(
        self,
        name: str
    ) -> bool:
        """
        Check provider existence.
        """

        return name in self.providers

    def count(self) -> int:
        """
        Return provider count.
        """

        return len(self.providers)
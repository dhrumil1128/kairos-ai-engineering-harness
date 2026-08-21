"""
File: core/providers/provider_factory.py

Purpose:
Create provider instances.

Why:

KAIROS supports multiple LLM
providers and needs a standard
creation mechanism.

Future:

V2:
- Dependency injection

V3:
- Configuration loading

V4:
- Dynamic providers

V5:
- Plugin providers
"""


class ProviderFactory:
    """
    Create provider instances.
    """

    def create(
        self,
        provider_name: str
    ) -> dict:
        """
        Create provider.

        Parameters:
            provider_name:
                Provider identifier.

        Returns:
            Provider configuration.
        """

        supported = {
            "openai": {
                "name": "openai"
            },
            "claude": {
                "name": "claude"
            },
            "gemini": {
                "name": "gemini"
            },
            "groq": {
                "name": "groq"
            },
            "ollama": {
                "name": "ollama"
            },
            
            "nvidia": {
            "name": "nvidia"
        },
        }

        return supported.get(
            provider_name.lower(),
            {}
        )

    def supported_providers(
        self
    ) -> list[str]:
        """
        Return supported providers.
        """

        return [
            "openai",
            "claude",
            "gemini",
            "groq",
            "ollama",
            "nvidia",
        ]
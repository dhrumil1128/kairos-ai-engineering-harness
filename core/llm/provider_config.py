"""
File: core/llm/provider_config.py

Purpose:
Load provider configuration from
providers.yaml and register providers.

Why:

Separates configuration from code.

Architecture:

providers.yaml
        ↓
ProviderConfig
        ↓
ProviderManager
        ↓
ModelRouter
        ↓
Agents

Version 1:

- Load YAML configuration
- Return provider configuration

Future Versions:

V2:
- Environment variable support

V3:
- Secret manager support

V4:
- Configuration validation

V5:
- Dynamic provider reload
"""

# YAML parsing.
import yaml

# Structured typing.
from typing import Dict, Any


class ProviderConfig:
    """
    Loads provider configuration.
    """

    def __init__(
        self,
        config_path: str
    ):
        """
        Initialize config loader.

        Parameters:
            config_path:
                Path to providers.yaml
        """

        self.config_path = config_path

    def load(self) -> Dict[str, Any]:
        """
        Load provider configuration.

        Returns:
            Dictionary containing
            provider settings.
        """

        with open(
            self.config_path,
            "r",
            encoding="utf-8"
        ) as file:

            return yaml.safe_load(file)
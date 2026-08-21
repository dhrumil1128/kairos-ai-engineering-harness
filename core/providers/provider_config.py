"""
File: core/providers/provider_config.py

Purpose:
Load provider configuration.

Why:

KAIROS should load provider
settings from providers.yaml
instead of hardcoding values.

Future:

V2:
- Environment variable support

V3:
- Secret manager integration

V4:
- Configuration validation

V5:
- Dynamic reload
"""

from pathlib import Path

import yaml


class ProviderConfig:
    """
    Manage provider configuration.
    """

    def __init__(
        self,
        config_path: str = (
            "config/providers.yaml"
        )
    ):
        """
        Initialize configuration.
        """

        self.config_path = (
            config_path
        )

    def load(
        self
    ) -> dict:
        """
        Load configuration.

        Returns:
            Provider configuration.
        """

        path = Path(
            self.config_path
        )

        if not path.exists():
            return {}

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            data = yaml.safe_load(
                file
            )

        return data or {}

    def exists(
        self
    ) -> bool:
        """
        Check configuration.
        """

        return Path(
            self.config_path
        ).exists()
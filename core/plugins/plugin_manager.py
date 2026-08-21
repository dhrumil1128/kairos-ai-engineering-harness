"""
File: core/plugins/plugin_manager.py

Purpose:
Manage KAIROS plugins.

Responsibilities:

- Register plugins
- Retrieve plugins
- List plugins

Future Versions:

V2:
- Dynamic loading

V3:
- Plugin discovery

V4:
- Plugin dependencies

V5:
- Marketplace support
"""


class PluginManager:
    """
    KAIROS plugin manager.
    """

    def __init__(self):
        """
        Initialize manager.
        """

        self._plugins = {}

    def register_plugin(
        self,
        name: str,
        plugin
    ) -> None:
        """
        Register plugin.
        """

        self._plugins[name] = plugin

    def get_plugin(
        self,
        name: str
    ):
        """
        Retrieve plugin.
        """

        return self._plugins.get(
            name
        )

    def has_plugin(
        self,
        name: str
    ) -> bool:
        """
        Check existence.
        """

        return (
            name
            in self._plugins
        )

    def list_plugins(
        self
    ) -> list[str]:
        """
        List plugins.
        """

        return list(
            self._plugins.keys()
        )
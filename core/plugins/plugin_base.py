"""
File: core/plugins/plugin_base.py

Purpose:
Base class for all KAIROS plugins.

All plugins should inherit
from this class.

Future Plugins:

- Filesystem Plugin
- Git Plugin
- Browser Plugin
- Security Plugin
- Testing Plugin
- Documentation Plugin
"""


class PluginBase:
    """
    Base plugin contract.
    """

    def __init__(
        self,
        name: str
    ):
        """
        Initialize plugin.
        """

        self.name = name

    def execute(
        self,
        *args,
        **kwargs
    ):
        """
        Execute plugin logic.

        Must be implemented
        by child plugins.
        """

        raise NotImplementedError(
            "Plugin must implement execute()."
        )
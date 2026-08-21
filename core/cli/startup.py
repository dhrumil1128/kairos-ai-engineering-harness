"""
File: core/cli/startup.py

Purpose:
Perform CLI startup checks.

Why:

Provides visibility into
system initialization.

Architecture:

Banner
 ↓
Startup
 ↓
Prompt
"""

from core.runtime.runtime_manager import (
    RuntimeManager
)



class Startup:
    """
    CLI startup manager.
    """

    def __init__(self):
        """
        Initialize startup.
        """

        self.runtime = (
            RuntimeManager()
        )
    
    
    
    def get_checks(
        self
    ) -> list[str]:
        """
        Return startup checks.
        """

        return [
            "Loading Agents",
            "Loading Memory",
            "Loading MCPs",
            "Loading Tools",
            "System Ready"
        ]

    def run(
    self
    ) -> list[str]:
        """
        Execute startup sequence.
        """

        self.runtime.initialize()

        return self.get_checks()
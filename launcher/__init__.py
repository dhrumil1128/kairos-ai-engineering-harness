"""
KAIROS desktop launcher package.

The launcher is a desktop bootstrapper only. It does not contain
KAIROS business logic, providers, agents, planning, memory, or
orchestration code.
"""

from launcher.launcher import Launcher, main

__all__ = [
    "Launcher",
    "main",
]

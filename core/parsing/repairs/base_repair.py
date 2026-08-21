"""
File: core/parsing/repairs/base_repair.py

Purpose:
Base class for JSON repair strategies.

Why:
Each repair strategy handles a specific
type of JSON syntax error. The base class
provides a common interface.

Architecture Position:

Parsing Subsystem
    ↓
JsonRepair (Base Class)
    ↓
Specific Repair Implementations
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class JsonRepair(ABC):
    """
    Base class for JSON repair strategies.

    Each subclass implements a specific repair
    for a particular type of JSON syntax error.

    Repairs are syntax-only - they do not
    fabricate or invent missing values.
    """

    def __init__(self):
        """Initialize the repair strategy."""
        self._repair_count = 0

    @abstractmethod
    def repair(self, text: str) -> str:
        """
        Attempt to repair the JSON text.

        Args:
            text: JSON text with potential syntax errors.

        Returns:
            Repaired JSON text (may be unchanged if no repair possible).
        """
        pass

    @property
    def name(self) -> str:
        """
        Get the repair strategy name.

        Returns:
            Name of this repair strategy.
        """
        return self.__class__.__name__

    @property
    def description(self) -> str:
        """
        Get a description of what this repair does.

        Returns:
            Description of the repair strategy.
        """
        return "Base JSON repair strategy"

    def get_repair_info(self) -> Dict[str, Any]:
        """
        Get information about the repair.

        Returns:
            Dictionary with repair information.
        """
        return {
            "name": self.name,
            "description": self.description,
            "repair_count": self._repair_count,
        }

    def _increment_repair_count(self) -> None:
        """Increment the repair counter."""
        self._repair_count += 1

    def can_repair(self, text: str) -> bool:
        """
        Check if this repair can be applied.

        Args:
            text: JSON text to check.

        Returns:
            True if this repair might help.
        """
        return True

    def get_priority(self) -> int:
        """
        Get the priority for this repair.

        Lower numbers run first in the pipeline.

        Returns:
            Priority value (default: 0).
        """
        return 0

    def reset_count(self) -> None:
        """Reset the repair counter."""
        self._repair_count = 0
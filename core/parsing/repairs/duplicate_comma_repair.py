"""
File: core/parsing/repairs/duplicate_comma_repair.py

Purpose:
Remove duplicate commas in JSON.

Why:
LLMs may accidentally include double commas
like ",," which is invalid JSON. This repair
removes the duplicates.

Architecture Position:

RepairPipeline
    ↓
DuplicateCommaRepair
"""

import re
from typing import Dict, Any

from core.parsing.repairs.base_repair import JsonRepair


class DuplicateCommaRepair(JsonRepair):
    """
    Repair for duplicate commas in JSON.

    Removes consecutive commas: ",," -> ","
    """

    # Pattern to match duplicate commas
    DUPLICATE_COMMA_PATTERN = re.compile(
        r",{2,}"
    )

    def repair(self, text: str) -> str:
        """
        Remove duplicate commas.

        Args:
            text: JSON text with potential duplicate commas.

        Returns:
            JSON text with duplicate commas removed.
        """
        if not text:
            return text

        repaired = self.DUPLICATE_COMMA_PATTERN.sub(",", text)

        # Track if we made changes
        if repaired != text:
            self._increment_repair_count()

        return repaired

    @property
    def description(self) -> str:
        """Get description of this repair."""
        return "Removes duplicate commas (, -> ,)"

    def can_repair(self, text: str) -> bool:
        """
        Check if text has duplicate commas.

        Args:
            text: JSON text to check.

        Returns:
            True if duplicate commas are likely present.
        """
        return bool(self.DUPLICATE_COMMA_PATTERN.search(text))

    def get_repair_info(self) -> Dict[str, Any]:
        """Get repair information."""
        info = super().get_repair_info()
        info.update({
            "type": "duplicate_comma",
            "pattern": self.DUPLICATE_COMMA_PATTERN.pattern,
        })
        return info
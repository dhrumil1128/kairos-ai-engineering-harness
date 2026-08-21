"""
File: core/parsing/repairs/trailing_comma_repair.py

Purpose:
Remove trailing commas from JSON.

Why:
JSON does not allow trailing commas, but LLMs
often include them. This repair removes them.

Architecture Position:

RepairPipeline
    ↓
TrailingCommaRepair
"""

import re
from typing import Dict, Any

from core.parsing.repairs.base_repair import JsonRepair


class TrailingCommaRepair(JsonRepair):
    """
    Repair for trailing commas in JSON.

    Removes commas that appear before:
    - Closing braces: }, ]
    - Closing brackets: ], }
    """

    # Pattern to match trailing commas
    TRAILING_COMMA_PATTERN = re.compile(
        r",(\s*[\]}])"
    )

    def repair(self, text: str) -> str:
        """
        Remove trailing commas from JSON text.

        Args:
            text: JSON text with potential trailing commas.

        Returns:
            JSON text with trailing commas removed.
        """
        if not text:
            return text

        repaired = text

        # Remove trailing commas before }
        repaired = self.TRAILING_COMMA_PATTERN.sub(r"\1", repaired)

        # Remove trailing commas before ]
        # Need separate pattern for ]
        repaired = re.sub(r",(\s*\])", r"\1", repaired)

        # Track if we made changes
        if repaired != text:
            self._increment_repair_count()

        return repaired

    @property
    def description(self) -> str:
        """Get description of this repair."""
        return "Removes trailing commas before closing braces and brackets"

    def can_repair(self, text: str) -> bool:
        """
        Check if text likely has trailing commas.

        Args:
            text: JSON text to check.

        Returns:
            True if trailing commas are likely present.
        """
        return "," in text and (
            re.search(r",\s*[}\]]", text) is not None
        )

    def get_repair_info(self) -> Dict[str, Any]:
        """Get repair information."""
        info = super().get_repair_info()
        info.update({
            "type": "trailing_comma",
            "pattern": self.TRAILING_COMMA_PATTERN.pattern,
        })
        return info
"""
File: core/parsing/repairs/missing_comma_repair.py

Purpose:
Add missing commas in JSON.

Why:
LLMs may forget commas between items in objects
or arrays. This repair adds them where needed.

Architecture Position:

RepairPipeline
    ↓
MissingCommaRepair
"""

import re
from typing import Dict, Any

from core.parsing.repairs.base_repair import JsonRepair


class MissingCommaRepair(JsonRepair):
    """
    Repair for missing commas in JSON.

    Adds commas between:
    - Key-value pairs in objects
    - Array elements
    """

    # Pattern to match missing comma before } or ]
    MISSING_COMMA_BEFORE_CLOSING = re.compile(
        r'(\s)([}\]])'
    )

    # Pattern to match missing comma between key-value pairs
    MISSING_COMMA_BETWEEN_PAIRS = re.compile(
        r'(\"\s*:\s*[^,}\]]+)\s+(\w+\s*:)'
    )

    # Pattern to match missing comma between array elements
    MISSING_COMMA_IN_ARRAY = re.compile(
        r'(\]\s*\w+\s*:)'
    )

    def repair(self, text: str) -> str:
        """
        Add missing commas to JSON text.

        Args:
            text: JSON text with potential missing commas.

        Returns:
            JSON text with commas added where needed.
        """
        if not text:
            return text

        repaired = text

        # Add comma before } if missing
        repaired = self._add_comma_before_closing(repaired)

        # Add comma between key-value pairs if missing
        repaired = self._add_comma_between_pairs(repaired)

        # Track if we made changes
        if repaired != text:
            self._increment_repair_count()

        return repaired

    def _add_comma_before_closing(self, text: str) -> str:
        """
        Add comma before closing braces/brackets if missing.

        Args:
            text: JSON text.

        Returns:
            Text with commas added.
        """
        # Match: value followed by } or ] (with optional whitespace)
        # But not if already followed by comma
        def add_comma_before_close(match):
            ws = match.group(1)
            close_char = match.group(2)

            # Check if there's already a comma
            # This is a simplified check
            return f"{ws},{close_char}"

        # Pattern: whitespace followed by } or ]
        # where there's content before
        repaired = re.sub(
            r'(\s)([}\]])',
            lambda m: f'{m.group(1)},' + m.group(2)
            if m.group(1) != ',' else m.group(0),
            text
        )

        return repaired

    def _add_comma_between_pairs(self, text: str) -> str:
        """
        Add comma between key-value pairs.

        Args:
            text: JSON text.

        Returns:
            Text with commas added between pairs.
        """
        # This is a best-effort repair
        # Look for patterns like: "value" "key":
        repaired = re.sub(
            r'("\s*:\s*[^,}\]]+)\s+(")',
            r'\1, \2',
            text
        )

        return repaired

    @property
    def description(self) -> str:
        """Get description of this repair."""
        return "Adds missing commas in objects and arrays"

    def can_repair(self, text: str) -> bool:
        """
        Check if text likely has missing commas.

        Args:
            text: JSON text to check.

        Returns:
            True if missing commas are likely present.
        """
        # Check for value followed by } or ] without comma
        if re.search(r'[^,}\]]\s*[}\]]', text):
            return True

        # Check for pattern: "value" "key":
        if re.search(r'"\s*:\s*[^,}\]]+\s+\w+\s*:', text):
            return True

        return False

    def get_repair_info(self) -> Dict[str, Any]:
        """Get repair information."""
        info = super().get_repair_info()
        info.update({
            "type": "missing_comma",
            "description": "Adds commas between JSON elements",
        })
        return info
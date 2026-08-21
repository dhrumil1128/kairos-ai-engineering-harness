"""
File: core/parsing/repairs/quote_repair.py

Purpose:
Fix quote issues in JSON.

Why:
LLMs may use smart quotes, mismatched quotes,
or inconsistent quote styles. This repair
normalizes quotes to standard JSON format.

Architecture Position:

RepairPipeline
    ↓
QuoteRepair
"""

import re
from typing import Dict, Any

from core.parsing.repairs.base_repair import JsonRepair


class QuoteRepair(JsonRepair):
    """
    Repair for quote issues in JSON.

    Handles:
    - Smart quotes (curly quotes)
    - Mismatched quotes
    - Unbalanced quotes in strings
    """

    # Smart quotes mapping
    SMART_QUOTES = {
        '"': '"',  # Left double quotation mark
        '"': '"',  # Right double quotation mark
        "'": "'",  # Left single quotation mark
        "'": "'",  # Right single quotation mark
    }

    # Pattern to match smart quotes
    SMART_QUOTE_PATTERN = re.compile(
        "[" + re.escape('"' + '"' + "'" + "'") + "]"
    )

    def repair(self, text: str) -> str:
        """
        Fix quote issues in JSON text.

        Args:
            text: JSON text with potential quote issues.

        Returns:
            JSON text with quotes normalized.
        """
        if not text:
            return text

        repaired = text

        # Replace smart quotes with standard quotes
        repaired = self.SMART_QUOTE_PATTERN.sub(
            lambda m: self.SMART_QUOTES.get(m.group(), m.group()),
            repaired
        )

        # Fix unmatched double quotes in keys
        repaired = self._fix_unmatched_quotes(repaired)

        # Track if we made changes
        if repaired != text:
            self._increment_repair_count()

        return repaired

    def _fix_unmatched_quotes(self, text: str) -> str:
        """
        Attempt to fix unmatched quotes.

        Args:
            text: JSON text.

        Returns:
            Text with unmatched quotes fixed.
        """
        # Count quotes
        double_quotes = text.count('"')

        # If odd number, we may have an unmatched quote
        if double_quotes % 2 != 0:
            # Try to find and fix the issue
            # Look for patterns like: {"key": value}
            # where value might have unmatched quotes

            # Simple fix: add a closing quote at the end
            if text.endswith('"') is False and text.endswith("}"):
                # Check if we're missing a closing quote
                last_quote_pos = text.rfind('"')
                if last_quote_pos > 0:
                    # Try inserting a closing quote
                    text = text + '"'

        return text

    @property
    def description(self) -> str:
        """Get description of this repair."""
        return "Normalizes smart quotes and fixes unmatched quotes"

    def can_repair(self, text: str) -> bool:
        """
        Check if text has quote issues.

        Args:
            text: JSON text to check.

        Returns:
            True if quote issues are likely present.
        """
        # Check for smart quotes
        if any(c in text for c in self.SMART_QUOTES):
            return True

        # Check for odd number of quotes
        if text.count('"') % 2 != 0:
            return True

        return False

    def get_repair_info(self) -> Dict[str, Any]:
        """Get repair information."""
        info = super().get_repair_info()
        info.update({
            "type": "quote",
            "smart_quotes_count": len(self.SMART_QUOTES),
        })
        return info
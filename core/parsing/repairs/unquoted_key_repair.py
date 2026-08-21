"""
File: core/parsing/repairs/unquoted_key_repair.py

Purpose:
Quote unquoted keys in JSON.

Why:
JSON requires all keys to be quoted strings.
LLMs may output keys without quotes. This repair
adds quotes where needed.

Architecture Position:

RepairPipeline
    ↓
UnquotedKeyRepair
"""

import re
from typing import Dict, Any

from core.parsing.repairs.base_repair import JsonRepair


class UnquotedKeyRepair(JsonRepair):
    """
    Repair for unquoted keys in JSON.

    Adds quotes around unquoted object keys.

    Note: This is a best-effort repair and may
    not handle all edge cases.
    """

    # Pattern to match unquoted keys
    # Matches: unquoted_word:
    UNQUOTED_KEY_PATTERN = re.compile(
        r'(?<!["\'])(\b[a-zA-Z_][a-zA-Z0-9_]*\b)\s*:'
    )

    # Pattern to identify already quoted keys (to skip)
    QUOTED_KEY_PATTERN = re.compile(
        r'["\'][^"\']*["\']\s*:'
    )

    def repair(self, text: str) -> str:
        """
        Add quotes around unquoted keys.

        Args:
            text: JSON text with potential unquoted keys.

        Returns:
            JSON text with keys quoted.
        """
        if not text:
            return text

        repaired = text

        # Find and quote unquoted keys
        # Must be at the start of a value (after { or ,)
        repaired = self._quote_unquoted_keys(repaired)

        # Track if we made changes
        if repaired != text:
            self._increment_repair_count()

        return repaired

    def _quote_unquoted_keys(self, text: str) -> str:
        """
        Quote unquoted object keys.

        Args:
            text: JSON text.

        Returns:
            Text with keys quoted.
        """
        # Match: { or , followed by unquoted word followed by :
        def quote_key(match):
            # Check if this is already quoted
            pos = match.start()

            # Look backwards for { or ,
            before = text[:pos]
            last_brace = max(before.rfind('{'), before.rfind(','))

            # If we found a { or , before this key, it's unquoted
            if last_brace >= 0:
                key = match.group(1)
                # Make sure it's not a keyword that looks like a key
                if key not in ('true', 'false', 'null'):
                    return f'"{key}"' + match.group(0)[len(key):]

            return match.group(0)

        # Apply the pattern
        repaired = self.UNQUOTED_KEY_PATTERN.sub(quote_key, text)

        return repaired

    @property
    def description(self) -> str:
        """Get description of this repair."""
        return "Adds quotes around unquoted object keys"

    def can_repair(self, text: str) -> bool:
        """
        Check if text has unquoted keys.

        Args:
            text: JSON text to check.

        Returns:
            True if unquoted keys are likely present.
        """
        # Look for pattern: word: at start of object
        # but not already quoted
        if not self.QUOTED_KEY_PATTERN.search(text):
            # No quoted keys found, might be all unquoted
            if self.UNQUOTED_KEY_PATTERN.search(text):
                return True

        # Check for mixed quoted/unquoted
        # Find a key that's not quoted
        lines = text.split('\n')
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('"') or stripped.startswith('['):
                continue
            if ':' in stripped and not stripped.startswith('"'):
                # Check if it's a key (not a string value)
                if re.match(r'^\w+\s*:', stripped):
                    return True

        return False

    def get_repair_info(self) -> Dict[str, Any]:
        """Get repair information."""
        info = super().get_repair_info()
        info.update({
            "type": "unquoted_key",
            "pattern": self.UNQUOTED_KEY_PATTERN.pattern,
        })
        return info
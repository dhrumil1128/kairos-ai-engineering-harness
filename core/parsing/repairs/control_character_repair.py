"""
File: core/parsing/repairs/control_character_repair.py

Purpose:
Remove control characters from JSON.

Why:
Control characters are invalid in JSON strings
and can cause parsing failures. This repair
removes or escapes them.

Architecture Position:

RepairPipeline
    ↓
ControlCharacterRepair
"""

import re
from typing import Dict, Any

from core.parsing.repairs.base_repair import JsonRepair


class ControlCharacterRepair(JsonRepair):
    """
    Repair for control characters in JSON.

    Removes or escapes control characters that are
    invalid in JSON strings.
    """

    # Pattern to match control characters (ASCII 0-31, except \t, \n, \r)
    CONTROL_CHARS = re.compile(
        r"[\x00-\x08\x0b\x0c\x0e-\x1f]"
    )

    # Pattern to match unescaped control characters in strings
    UNESCAPED_CONTROL = re.compile(
        r'(?<!\\)[\x00-\x1f]'
    )

    def repair(self, text: str) -> str:
        """
        Remove or escape control characters.

        Args:
            text: JSON text with potential control characters.

        Returns:
            JSON text with control characters removed.
        """
        if not text:
            return text

        repaired = text

        # Remove control characters
        repaired = self.CONTROL_CHARS.sub("", repaired)

        # Track if we made changes
        if repaired != text:
            self._increment_repair_count()

        return repaired

    @property
    def description(self) -> str:
        """Get description of this repair."""
        return "Removes control characters (ASCII 0-31) from JSON"

    def can_repair(self, text: str) -> bool:
        """
        Check if text has control characters.

        Args:
            text: JSON text to check.

        Returns:
            True if control characters are likely present.
        """
        return bool(self.CONTROL_CHARS.search(text))

    def escape_control_chars(self, text: str) -> str:
        """
        Escape control characters instead of removing them.

        Args:
            text: JSON text with control characters.

        Returns:
            JSON text with control characters escaped.
        """
        def escape_char(match):
            char = match.group()
            code = ord(char)
            return f"\\u{code:04x}"

        return self.UNESCAPED_CONTROL.sub(escape_char, text)

    def get_repair_info(self) -> Dict[str, Any]:
        """Get repair information."""
        info = super().get_repair_info()
        info.update({
            "type": "control_character",
            "pattern": self.CONTROL_CHARS.pattern,
        })
        return info
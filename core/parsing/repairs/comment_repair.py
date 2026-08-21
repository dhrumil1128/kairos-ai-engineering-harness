"""
File: core/parsing/repairs/comment_repair.py

Purpose:
Remove comments from JSON.

Why:
JSON does not support comments, but LLMs
often include them in their output. This repair
removes them to produce valid JSON.

Architecture Position:

RepairPipeline
    ↓
CommentRepair
"""

import re
from typing import Dict, Any

from core.parsing.repairs.base_repair import JsonRepair


class CommentRepair(JsonRepair):
    """
    Repair for comments in JSON.

    Removes:
    - Single-line comments: // ...
    - Multi-line comments: /* ... */
    - Hash comments: # ...
    """

    # Pattern for single-line comments
    SINGLE_LINE_COMMENT = re.compile(
        r"//.*$",
        re.MULTILINE
    )

    # Pattern for multi-line comments
    MULTI_LINE_COMMENT = re.compile(
        r"/\*.*?\*/",
        re.DOTALL
    )

    # Pattern for hash comments
    HASH_COMMENT = re.compile(
        r"#.*$",
        re.MULTILINE
    )

    def repair(self, text: str) -> str:
        """
        Remove comments from JSON text.

        Args:
            text: JSON text with potential comments.

        Returns:
            JSON text with comments removed.
        """
        if not text:
            return text

        repaired = text

        # Remove multi-line comments first
        repaired = self.MULTI_LINE_COMMENT.sub("", repaired)

        # Remove single-line comments
        repaired = self.SINGLE_LINE_COMMENT.sub("", repaired)

        # Remove hash comments
        repaired = self.HASH_COMMENT.sub("", repaired)

        # Clean up empty lines
        repaired = re.sub(r"\n{3,}", "\n\n", repaired)

        # Track if we made changes
        if repaired != text:
            self._increment_repair_count()

        return repaired

    @property
    def description(self) -> str:
        """Get description of this repair."""
        return "Removes //, /* */, and # comments from JSON"

    def can_repair(self, text: str) -> bool:
        """
        Check if text has comments.

        Args:
            text: JSON text to check.

        Returns:
            True if comments are likely present.
        """
        return bool(
            self.SINGLE_LINE_COMMENT.search(text) or
            self.MULTI_LINE_COMMENT.search(text) or
            self.HASH_COMMENT.search(text)
        )

    def get_repair_info(self) -> Dict[str, Any]:
        """Get repair information."""
        info = super().get_repair_info()
        info.update({
            "type": "comment",
            "patterns": [
                self.SINGLE_LINE_COMMENT.pattern,
                self.MULTI_LINE_COMMENT.pattern,
                self.HASH_COMMENT.pattern,
            ],
        })
        return info
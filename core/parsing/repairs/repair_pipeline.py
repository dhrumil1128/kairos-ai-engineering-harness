"""
File: core/parsing/repairs/repair_pipeline.py

Purpose:
Pipeline that executes multiple repair strategies.

Why:
JSON errors can be complex. Running multiple
repair strategies in sequence increases the
chance of successful repair.

Architecture Position:

Parsing Subsystem
    ↓
RepairPipeline
    ↓
Multiple JsonRepair strategies
"""

from typing import List, Dict, Any, Optional
import json

from core.parsing.repairs.base_repair import JsonRepair
from core.parsing.repairs.trailing_comma_repair import TrailingCommaRepair
from core.parsing.repairs.missing_comma_repair import MissingCommaRepair
from core.parsing.repairs.duplicate_comma_repair import DuplicateCommaRepair
from core.parsing.repairs.quote_repair import QuoteRepair
from core.parsing.repairs.comment_repair import CommentRepair
from core.parsing.repairs.control_character_repair import ControlCharacterRepair
from core.parsing.repairs.unquoted_key_repair import UnquotedKeyRepair


class RepairPipeline:
    """
    Pipeline that executes JSON repair strategies.

    Repairs are executed in priority order until
    either the JSON parses successfully or all
    repairs are exhausted.

    Each repair is syntax-only - no value fabrication.
    """

    def __init__(
        self,
        repairs: Optional[List[JsonRepair]] = None
    ):
        """
        Initialize the repair pipeline.

        Args:
            repairs: Optional list of repair strategies.
                     Uses defaults if not provided.
        """
        self._repairs: List[JsonRepair] = repairs or self._default_repairs()
        self._history: List[Dict[str, Any]] = []
        self._successful_repairs: int = 0

    def _default_repairs(self) -> List[JsonRepair]:
        """
        Get the default list of repairs.

        Returns:
            List of default repair strategies.
        """
        return [
            CommentRepair(),
            ControlCharacterRepair(),
            TrailingCommaRepair(),
            MissingCommaRepair(),
            DuplicateCommaRepair(),
            QuoteRepair(),
            UnquotedKeyRepair(),
        ]

    def repair(self, text: str) -> str:
        """
        Attempt to repair JSON text.

        Executes repairs in priority order until
        successful or all repairs exhausted.

        Args:
            text: JSON text with potential syntax errors.

        Returns:
            Best-effort repaired JSON text.
        """
        if not text:
            return text

        current_text = text
        self._history = []
        self._successful_repairs = 0

        # Sort repairs by priority
        sorted_repairs = sorted(
            self._repairs,
            key=lambda r: r.get_priority()
        )

        for repair in sorted_repairs:
            # Check if this repair can apply
            if not repair.can_repair(current_text):
                continue

            # Apply repair
            repaired_text = repair.repair(current_text)

            # Record in history if changed
            if repaired_text != current_text:
                self._history.append({
                    "repair": repair.name,
                    "before": current_text[:200],  # Truncate for history
                    "after": repaired_text[:200],
                })
                current_text = repaired_text
                self._successful_repairs += 1

            # Check if JSON is now valid
            try:
                json.loads(current_text)
                return current_text
            except json.JSONDecodeError:
                continue

        # Return best-effort result
        return current_text

    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get repair history.

        Returns:
            List of repair history entries.
        """
        return self._history.copy()

    def get_repair_count(self) -> int:
        """
        Get total number of repairs applied.

        Returns:
            Number of repairs applied.
        """
        return self._successful_repairs

    def add_repair(self, repair: JsonRepair) -> None:
        """
        Add a repair strategy to the pipeline.

        Args:
            repair: Repair strategy to add.
        """
        self._repairs.append(repair)

    def remove_repair(self, repair_name: str) -> bool:
        """
        Remove a repair strategy by name.

        Args:
            repair_name: Name of repair to remove.

        Returns:
            True if repair was found and removed.
        """
        for i, repair in enumerate(self._repairs):
            if repair.name == repair_name:
                del self._repairs[i]
                return True
        return False

    def clear_history(self) -> None:
        """Clear repair history."""
        self._history = []
        self._successful_repairs = 0

    def get_repair_stats(self) -> Dict[str, Any]:
        """
        Get statistics about repairs.

        Returns:
            Dictionary with repair statistics.
        """
        repair_counts: Dict[str, int] = {}
        for entry in self._history:
            name = entry.get("repair", "unknown")
            repair_counts[name] = repair_counts.get(name, 0) + 1

        return {
            "total_repairs": self._successful_repairs,
            "repair_types": repair_counts,
            "history_length": len(self._history),
        }
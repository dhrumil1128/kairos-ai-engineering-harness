"""
File: core/parsing/repairs/__init__.py

Purpose:
Initialize the repairs package.

Why:
Exports all repair classes for easy importing.

Architecture Position:

Parsing Subsystem
    ↓
Repairs Package
"""

from core.parsing.repairs.base_repair import JsonRepair
from core.parsing.repairs.repair_pipeline import RepairPipeline
from core.parsing.repairs.trailing_comma_repair import TrailingCommaRepair
from core.parsing.repairs.quote_repair import QuoteRepair
from core.parsing.repairs.comment_repair import CommentRepair
from core.parsing.repairs.control_character_repair import ControlCharacterRepair
from core.parsing.repairs.missing_comma_repair import MissingCommaRepair
from core.parsing.repairs.duplicate_comma_repair import DuplicateCommaRepair
from core.parsing.repairs.unquoted_key_repair import UnquotedKeyRepair

__all__ = [
    "JsonRepair",
    "RepairPipeline",
    "TrailingCommaRepair",
    "QuoteRepair",
    "CommentRepair",
    "ControlCharacterRepair",
    "MissingCommaRepair",
    "DuplicateCommaRepair",
    "UnquotedKeyRepair",
]
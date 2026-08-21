"""
File: core/parsing/__init__.py

Purpose:
Public API for the Structured Output Parsing subsystem.

Why:
Provides a clean, well-documented interface for parsing
LLM structured output across all KAIROS components.

Architecture Position:

Providers
    ↓
Structured Output Parser
    ↓
ParseResult
    ↓
Agent Processing
"""

from core.parsing.parser_config import ParserConfig
from core.parsing.parse_result import ParseResult
from core.parsing.structured_output_parser import StructuredOutputParser
from core.parsing.json_normalizer import JsonNormalizer
from core.parsing.json_extractor import JsonExtractor
from core.parsing.schema_validator import SchemaValidator
from core.parsing.retry_prompt import RetryPrompt
from core.parsing.metrics import ParserMetrics
from core.parsing.repairs.base_repair import JsonRepair
from core.parsing.repairs.trailing_comma_repair import TrailingCommaRepair
from core.parsing.repairs.quote_repair import QuoteRepair
from core.parsing.repairs.comment_repair import CommentRepair
from core.parsing.repairs.control_character_repair import ControlCharacterRepair
from core.parsing.repairs.missing_comma_repair import MissingCommaRepair
from core.parsing.repairs.duplicate_comma_repair import DuplicateCommaRepair
from core.parsing.repairs.unquoted_key_repair import UnquotedKeyRepair
from core.parsing.repairs.repair_pipeline import RepairPipeline

__all__ = [
    # Main parser
    "StructuredOutputParser",
    "ParserConfig",
    "ParseResult",

    # Pipeline components
    "JsonNormalizer",
    "JsonExtractor",
    "SchemaValidator",
    "RetryPrompt",

    # Metrics
    "ParserMetrics",

    # Repair system
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
"""
File: core/parsing/parser_config.py

Purpose:
Configuration for the Structured Output Parser.

Why:
Parser behavior must be configurable without
modifying code. Different use cases need
different parsing strategies.

Architecture Position:

Structured Output Parser
    ↓
Parser Config
"""

from dataclasses import dataclass, field
from typing import Callable, Any, Optional
import logging


@dataclass
class ParserConfig:
    """
    Configuration for structured output parsing.

    Controls which parsing stages are enabled,
    retry behavior, and logging level.

    Attributes:
        enable_native_json: Use Python's native json module
            for initial parsing attempt.
        enable_repair: Enable the repair pipeline when
            JSON parsing fails.
        enable_retry: Enable retry callback when
            parsing fails completely.
        enable_schema_validation: Validate parsed data
            against an optional schema.
        enable_metrics: Track parsing metrics.
        max_retry_attempts: Maximum number of retry attempts.
        strict_mode: Fail fast on parse errors instead of
            attempting repairs.
        log_level: Logging level for parser operations.
    """

    # Stage 1-5: JSON parsing
    enable_native_json: bool = True

    # Stage 4: Repair pipeline
    enable_repair: bool = True

    # Stage 7: Retry callback
    enable_retry: bool = False

    # Stage 6: Schema validation
    enable_schema_validation: bool = True

    # Metrics tracking
    enable_metrics: bool = True

    # Retry configuration
    max_retry_attempts: int = 3

    # Strict mode options
    strict_mode: bool = False

    # Logging
    log_level: int = logging.INFO

    # Optional schema for validation
    schema: Optional[dict[str, Any]] = None

    # Optional retry callback
    retry_callback: Optional[Callable[[str, dict], Any]] = None

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if self.max_retry_attempts < 0:
            raise ValueError("max_retry_attempts must be >= 0")

        if self.retry_callback is not None and not self.enable_retry:
            raise ValueError(
                "retry_callback requires enable_retry=True"
            )

    @classmethod
    def strict(cls) -> "ParserConfig":
        """
        Create a strict configuration.

        No repairs, no retries, schema validation enabled.
        Useful for critical data paths.
        """
        return cls(
            enable_native_json=True,
            enable_repair=False,
            enable_retry=False,
            enable_schema_validation=True,
            strict_mode=True,
        )

    @classmethod
    def lenient(cls) -> "ParserConfig":
        """
        Create a lenient configuration.

        All repairs and retries enabled.
        Useful for debugging assistance.
        """
        return cls(
            enable_native_json=True,
            enable_repair=True,
            enable_retry=True,
            enable_schema_validation=True,
            strict_mode=False,
        )

    @classmethod
    def minimal(cls) -> "ParserConfig":
        """
        Create a minimal configuration.

        No repairs, no retries, no validation.
        Fastest parsing, least robust.
        """
        return cls(
            enable_native_json=True,
            enable_repair=False,
            enable_retry=False,
            enable_schema_validation=False,
            strict_mode=True,
        )
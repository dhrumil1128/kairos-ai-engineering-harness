"""
File: core/parsing/parse_result.py

Purpose:
Result container for structured output parsing.

Why:
Parsing can succeed or fail at multiple stages.
ParseResult provides a consistent interface for
all parsing outcomes.

Architecture Position:

Structured Output Parser
    ↓
ParseResult
    ↓
Agent Processing
"""

from dataclasses import dataclass, field
from typing import Any, Optional, List
from enum import Enum


class ParseStage(str, Enum):
    """
    Stage at which parsing completed or failed.

    Used to track parser progress through the pipeline.
    """

    INITIAL = "initial"
    NORMALIZED = "normalized"
    EXTRACTED = "extracted"
    STRICT_PARSED = "strict_parsed"
    REPAIRED = "repaired"
    RETRY = "retry"
    VALIDATED = "validated"
    FAILED = "failed"


@dataclass
class ParseResult:
    """
    Result of structured output parsing.

    Contains the parsed data (if successful) and
    detailed information about the parsing process.

    Attributes:
        success: Whether parsing succeeded.
        data: Parsed data (dict, list, or primitive).
        confidence: Confidence score (0.00-1.00).
        stage: Stage at which parsing completed.
        raw_response: Original LLM response.
        normalized_response: Response after normalization.
        extracted_json: JSON string after extraction.
        repaired_response: JSON after repair pipeline.
        repair_history: List of repairs applied.
        failure_reason: Reason for failure (if any).
        retry_count: Number of retries attempted.
        parse_time_ms: Total parsing time in milliseconds.
    """

    success: bool = False
    data: Optional[Any] = None
    confidence: float = 0.0
    stage: ParseStage = ParseStage.FAILED
    raw_response: str = ""
    normalized_response: str = ""
    extracted_json: str = ""
    repaired_response: str = ""
    repair_history: List[dict[str, str]] = field(
        default_factory=list
    )
    failure_reason: str = ""
    retry_count: int = 0
    parse_time_ms: float = 0.0

    def __post_init__(self) -> None:
        """Ensure confidence is within valid range."""
        if self.confidence < 0.0:
            self.confidence = 0.0
        if self.confidence > 1.0:
            self.confidence = 1.0

    @classmethod
    def success_result(
        cls,
        data: Any,
        confidence: float = 1.0,
        stage: ParseStage = ParseStage.STRICT_PARSED,
        **kwargs
    ) -> "ParseResult":
        """
        Create a successful parse result.

        Args:
            data: Parsed data.
            confidence: Confidence score (default 1.0).
            stage: Stage at which parsing succeeded.
            **kwargs: Additional fields to set.

        Returns:
            Successful ParseResult.
        """
        return cls(
            success=True,
            data=data,
            confidence=confidence,
            stage=stage,
            **kwargs
        )

    @classmethod
    def failure_result(
        cls,
        failure_reason: str,
        stage: ParseStage = ParseStage.FAILED,
        **kwargs
    ) -> "ParseResult":
        """
        Create a failed parse result.

        Args:
            failure_reason: Reason for failure.
            stage: Stage at which parsing failed.
            **kwargs: Additional fields to set.

        Returns:
            Failed ParseResult.
        """
        return cls(
            success=False,
            data=None,
            confidence=0.0,
            stage=stage,
            failure_reason=failure_reason,
            **kwargs
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert result to dictionary.

        Returns:
            Dictionary representation of the result.
        """
        return {
            "success": self.success,
            "data": self.data,
            "confidence": self.confidence,
            "stage": self.stage.value if isinstance(self.stage, ParseStage) else self.stage,
            "raw_response": self.raw_response,
            "normalized_response": self.normalized_response,
            "extracted_json": self.extracted_json,
            "repaired_response": self.repaired_response,
            "repair_history": self.repair_history,
            "failure_reason": self.failure_reason,
            "retry_count": self.retry_count,
            "parse_time_ms": self.parse_time_ms,
        }

    def merge(
        self,
        other: "ParseResult"
    ) -> "ParseResult":
        """
        Merge another result into this one.

        Used for combining retry results with earlier stages.

        Args:
            other: Another ParseResult to merge.

        Returns:
            Merged ParseResult.
        """
        merged = ParseResult(
            success=self.success or other.success,
            data=other.data if other.data is not None else self.data,
            confidence=other.confidence if other.confidence > self.confidence else self.confidence,
            stage=other.stage if other.stage != ParseStage.FAILED else self.stage,
            raw_response=self.raw_response or other.raw_response,
            normalized_response=self.normalized_response or other.normalized_response,
            extracted_json=self.extracted_json or other.extracted_json,
            repaired_response=self.repaired_response or other.repaired_response,
            repair_history=self.repair_history + other.repair_history,
            failure_reason=other.failure_reason or self.failure_reason,
            retry_count=max(self.retry_count, other.retry_count),
            parse_time_ms=self.parse_time_ms + other.parse_time_ms,
        )
        return merged
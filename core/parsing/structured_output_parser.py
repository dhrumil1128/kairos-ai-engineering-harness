"""
File: core/parsing/structured_output_parser.py

Purpose:
Main parser for structured output from LLM responses.

Why:
LLMs often return malformed JSON. This parser handles
normalization, extraction, repair, and validation in
a single pipeline.

Architecture Position:

Providers
    ↓
Structured Output Parser
    ↓
ParseResult
    ↓
Agent Processing
"""

import json
import re
import time
import logging
from typing import Any, Optional, Callable

from core.parsing.parser_config import ParserConfig
from core.parsing.parse_result import ParseResult, ParseStage
from core.parsing.json_normalizer import JsonNormalizer
from core.parsing.json_extractor import JsonExtractor
from core.parsing.schema_validator import SchemaValidator
from core.parsing.retry_prompt import RetryPrompt
from core.parsing.metrics import ParserMetrics
from core.parsing.repairs.repair_pipeline import RepairPipeline


class StructuredOutputParser:
    """
    Parser for structured LLM output.

    Implements the 8-stage parsing pipeline:
    1. Normalize
    2. Extract JSON
    3. Strict Parse
    4. Repair Pipeline
    5. Strict Parse Again
    6. Schema Validation
    7. Optional Retry Callback
    8. Return ParseResult

    Never throws JSONDecodeError. Never crashes.
    """

    def __init__(
        self,
        config: Optional[ParserConfig] = None,
        provider: str = "unknown",
        model: str = "unknown"
    ):
        """
        Initialize the structured output parser.

        Args:
            config: Parser configuration. Uses defaults if None.
            provider: Provider name for metrics.
            model: Model name for metrics.
        """
        self.config = config or ParserConfig()
        self.provider = provider
        self.model = model
        self.logger = logging.getLogger(__name__)

        # Initialize pipeline components
        self.normalizer = JsonNormalizer()
        self.extractor = JsonExtractor()
        self.validator = SchemaValidator()
        self.repair_pipeline = RepairPipeline()

        # Initialize metrics
        self.metrics = ParserMetrics(
            provider=provider,
            model=model,
            enabled=self.config.enable_metrics
        )

    def parse(
        self,
        raw_response: str
    ) -> ParseResult:
        """
        Parse raw LLM response into structured data.

        Implements the full 8-stage parsing pipeline.

        Args:
            raw_response: Raw LLM output text.

        Returns:
            ParseResult with success status and parsed data.
        """
        start_time = time.time()
        result = ParseResult(raw_response=raw_response)

        # Stage 1: Normalize
        if not self.config.strict_mode:
            normalized = self.normalizer.normalize(raw_response)
            result.normalized_response = normalized
            result.stage = ParseStage.NORMALIZED
        else:
            normalized = raw_response

        # Stage 2: Extract JSON
        extracted = self.extractor.extract(normalized)
        result.extracted_json = extracted
        result.stage = ParseStage.EXTRACTED

        # Stage 3: Strict Parse
        try:
            data = json.loads(extracted)
            result.data = data
            result.stage = ParseStage.STRICT_PARSED
            result.confidence = 1.0
            result.success = True

            # Track success
            self.metrics.record_strict_success()

            # Stage 6: Schema Validation
            if self.config.enable_schema_validation:
                validation_result = self.validator.validate(
                    data,
                    self.config.schema
                )
                if validation_result.success:
                    result.stage = ParseStage.VALIDATED
                else:
                    result.failure_reason = validation_result.failure_reason
                    result.confidence = 0.0
                    result.success = False
                    self.metrics.record_failure()

            # Calculate parse time
            result.parse_time_ms = (time.time() - start_time) * 1000

            # Stage 8: Return result
            self.metrics.record_parse_time(result.parse_time_ms)
            return result

        except json.JSONDecodeError:
            # Stage 4: Repair Pipeline
            if self.config.enable_repair:
                repaired = self.repair_pipeline.repair(extracted)
                result.repaired_response = repaired
                result.repair_history = self.repair_pipeline.get_history()
                result.stage = ParseStage.REPAIRED

                # Stage 5: Strict Parse Again
                try:
                    data = json.loads(repaired)
                    result.data = data
                    result.confidence = 0.90  # Repair confidence
                    result.success = True

                    self.metrics.record_repair_success()

                    # Stage 6: Schema Validation
                    if self.config.enable_schema_validation:
                        validation_result = self.validator.validate(
                            data,
                            self.config.schema
                        )
                        if validation_result.success:
                            result.stage = ParseStage.VALIDATED
                        else:
                            result.failure_reason = validation_result.failure_reason
                            result.confidence = 0.0
                            result.success = False
                            self.metrics.record_failure()

                    # Calculate parse time
                    result.parse_time_ms = (time.time() - start_time) * 1000

                    self.metrics.record_parse_time(result.parse_time_ms)
                    return result

                except json.JSONDecodeError as e:
                    result.failure_reason = f"Repair failed: {str(e)}"

            # Stage 7: Retry Callback
            if self.config.enable_retry and self.config.retry_callback:
                attempt = 0
                while attempt < self.config.max_retry_attempts:
                    attempt += 1
                    result.retry_count = attempt

                    try:
                        retry_data = self.config.retry_callback(
                            result.raw_response,
                            result.to_dict()
                        )

                        if retry_data is not None:
                            result.data = retry_data
                            result.confidence = 0.75  # Retry confidence
                            result.stage = ParseStage.RETRY
                            result.success = True
                            result.retry_count = attempt

                            self.metrics.record_retry_success()

                            # Calculate parse time
                            result.parse_time_ms = (time.time() - start_time) * 1000

                            self.metrics.record_parse_time(result.parse_time_ms)
                            return result

                    except Exception as e:
                        self.logger.debug(
                            f"Retry attempt {attempt} failed: {e}"
                        )

            # Stage 8: Return failure result
            result.stage = ParseStage.FAILED
            result.failure_reason = result.failure_reason or "Failed to parse JSON after all attempts"
            result.confidence = 0.0
            result.success = False

            self.metrics.record_failure()

        # Calculate parse time
        result.parse_time_ms = (time.time() - start_time) * 1000

        # Record metrics
        self.metrics.record_parse_time(result.parse_time_ms)

        return result

    def get_metrics(self) -> dict[str, Any]:
        """
        Get parsing metrics.

        Returns:
            Dictionary of metrics.
        """
        return self.metrics.to_dict()

    def reset_metrics(self) -> None:
        """Reset parsing metrics."""
        self.metrics.reset()
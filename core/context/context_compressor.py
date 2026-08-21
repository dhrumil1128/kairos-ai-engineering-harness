"""
File: core/context/context_compressor.py

Purpose:
Compress project context
before prompt construction.

Why:

Only the highest-value
context should be sent
to the LLM.

Architecture:

Ranked Context
        │
        ▼
Context Compressor
        │
        ├── Remove Empty
        ├── Remove Duplicate
        ├── Apply Limit
        ├── Compression Report
        │
        ▼
Prompt Builder

V2:
- Semantic Compression

V3:
- LLM Summarization

V4:
- Hierarchical Compression

V5:
- Adaptive Compression
"""

from __future__ import annotations

from core.logging.kairos_logger import (
    KairosLogger,
)


class ContextCompressor:
    """
    Enterprise Context
    Compressor.
    """

    def __init__(
        self
    ):
        """
        Initialize
        compressor.
        """

        self.logger = (
            KairosLogger(
                "context"
            )
        )

    # ---------------------------------- #
    # Compress Context
    # ---------------------------------- #

    def compress(
        self,
        contexts: list[str],
        max_items: int = 5
    ) -> list[str]:
        """
        Compress ranked
        context.
        """

        self.logger.info(
            "Compressing context."
        )

        contexts = (
            self.remove_empty(
                contexts
            )
        )

        contexts = (
            self.remove_duplicates(
                contexts
            )
        )

        compressed = (
            contexts[:max_items]
        )

        self.logger.success(
            "Context compressed."
        )

        return compressed

    # ---------------------------------- #
    # Remove Empty
    # ---------------------------------- #

    def remove_empty(
        self,
        contexts: list[str]
    ) -> list[str]:
        """
        Remove empty
        context items.
        """

        return [

            context

            for context
            in contexts

            if context.strip()

        ]

    # ---------------------------------- #
    # Remove Duplicates
    # ---------------------------------- #

    def remove_duplicates(
        self,
        contexts: list[str]
    ) -> list[str]:
        """
        Remove duplicate
        context.
        """

        return list(
            dict.fromkeys(
                contexts
            )
        )
        
    # ---------------------------------- #
    # Compression Ratio
    # ---------------------------------- #

    def compression_ratio(
        self,
        original_count: int,
        compressed_count: int
    ) -> float:
        """
        Calculate
        compression ratio.
        """

        if original_count == 0:

            return 0.0

        return (

            compressed_count
            / original_count

        )

    # ---------------------------------- #
    # Compression Report
    # ---------------------------------- #

    def report(
        self,
        original: list[str],
        compressed: list[str]
    ) -> dict:
        """
        Return compression
        statistics.
        """

        return {

            "original_items":
            len(original),

            "compressed_items":
            len(compressed),

            "compression_ratio":
            self.compression_ratio(
                len(original),
                len(compressed)
            ),

        }

    # ---------------------------------- #
    # Reset Compressor
    # ---------------------------------- #

    def clear(
        self
    ) -> None:
        """
        Reset Context
        Compressor.
        """

        self.logger.info(
            "Context Compressor reset."
        )
        
        
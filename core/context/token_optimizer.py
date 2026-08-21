"""
File: core/context/token_optimizer.py

Purpose:
Estimate and optimize
token usage before
sending prompts to
LLMs.

Why:

Efficient token usage
reduces latency and
API cost while keeping
high-value context.

Architecture:

Context
    │
    ▼
Token Optimizer
    │
    ├── Token Estimation
    ├── Budget Validation
    ├── Context Trimming
    ├── Budget Report
    │
    ▼
Prompt Builder

V2:
- Model-specific tokenizers

V3:
- Cost estimation

V4:
- Dynamic token budgeting

V5:
- Multi-model optimization
"""

from __future__ import annotations

from core.logging.kairos_logger import (
    KairosLogger,
)


class TokenOptimizer:
    """
    Enterprise Token
    Optimizer.
    """

    def __init__(
        self
    ):
        """
        Initialize optimizer.
        """

        self.logger = (
            KairosLogger(
                "context"
            )
        )

    # ---------------------------------- #
    # Estimate Tokens
    # ---------------------------------- #

    def estimate_tokens(
        self,
        text: str
    ) -> int:
        """
        Estimate token
        count.
        """

        if not text:

            return 0

        words = len(
            text.split()
        )

        tokens = int(
            words * 1.33
        )

        self.logger.info(
            f"Estimated Tokens: {tokens}"
        )

        return tokens

    # ---------------------------------- #
    # Budget Validation
    # ---------------------------------- #

    def fits_budget(
        self,
        text: str,
        max_tokens: int
    ) -> bool:
        """
        Validate token
        budget.
        """

        return (

            self.estimate_tokens(
                text
            )

            <= max_tokens

        )

    # ---------------------------------- #
    # Remaining Budget
    # ---------------------------------- #

    def remaining_budget(
        self,
        text: str,
        max_tokens: int
    ) -> int:
        """
        Remaining token
        budget.
        """

        return (

            max_tokens

            - self.estimate_tokens(
                text
            )

        )

    # ---------------------------------- #
    # Trim Context
    # ---------------------------------- #

    def trim_context(
        self,
        contexts: list[str],
        max_tokens: int
    ) -> list[str]:
        """
        Trim context
        until it fits
        the budget.
        """

        optimized = []

        used = 0

        for context in contexts:

            tokens = (
                self.estimate_tokens(
                    context
                )
            )

            if (

                used + tokens

                > max_tokens

            ):

                break

            optimized.append(
                context
            )

            used += tokens

        self.logger.success(
            "Token optimization completed."
        )

        return optimized
    
    
        # ---------------------------------- #
    # Optimization Report
    # ---------------------------------- #

    def report(
        self,
        original: list[str],
        optimized: list[str]
    ) -> dict:
        """
        Return token
        optimization report.
        """

        original_tokens = sum(

            self.estimate_tokens(
                context
            )

            for context
            in original

        )

        optimized_tokens = sum(

            self.estimate_tokens(
                context
            )

            for context
            in optimized

        )

        return {

            "original_items":
            len(original),

            "optimized_items":
            len(optimized),

            "original_tokens":
            original_tokens,

            "optimized_tokens":
            optimized_tokens,

            "saved_tokens":
            (
                original_tokens
                - optimized_tokens
            ),

        }

    # ---------------------------------- #
    # Reset Optimizer
    # ---------------------------------- #

    def clear(
        self
    ) -> None:
        """
        Reset Token
        Optimizer.
        """

        self.logger.info(
            "Token Optimizer reset."
        )
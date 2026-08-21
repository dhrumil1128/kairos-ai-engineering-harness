"""
File: core/context/context_ranker.py

Purpose:
Rank available context
by relevance before
building the final
LLM prompt.

Why:

Large projects contain
far more context than
can be sent to the LLM.

The Context Ranker scores
every context item and
keeps only the most
relevant information.

Architecture:

Context Loader
        │
        ▼
Context Ranker
        │
        ├── Keyword Score
        ├── File Score
        ├── Metadata Score
        ├── Final Ranking
        │
        ▼
Prompt Builder

V2:
- Embedding Ranking

V3:
- Semantic Ranking

V4:
- Hybrid Ranking

V5:
- Learning-Based Ranking
"""

from __future__ import annotations

from core.logging.kairos_logger import (
    KairosLogger,
)


class ContextRanker:
    """
    Enterprise Context
    Ranker.
    """

    def __init__(
        self
    ):
        """
        Initialize ranker.
        """

        self.logger = (
            KairosLogger(
                "context"
            )
        )

    # ---------------------------------- #
    # Rank Context
    # ---------------------------------- #

    def rank(
        self,
        contexts: list[str],
        query: str
    ) -> list[str]:
        """
        Rank context
        using keyword
        relevance.
        """

        self.logger.info(
            "Ranking context."
        )

        query_words = {

            word.lower()

            for word
            in query.split()

        }

        scored = []

        for context in contexts:

            score = (
                self._score_context(
                    context,
                    query_words
                )
            )

            scored.append(

                (
                    score,
                    context
                )

            )

        scored.sort(

            reverse=True,

            key=lambda item:
            item[0]

        )

        self.logger.success(
            "Ranking completed."
        )

        return [

            item[1]

            for item
            in scored

        ]

    # ---------------------------------- #
    # Score Context
    # ---------------------------------- #

    def _score_context(
        self,
        context: str,
        query_words: set[str]
    ) -> int:
        """
        Calculate
        relevance score.
        """

        text = (
            context.lower()
        )

        score = 0

        for word in query_words:

            if word in text:

                score += 1

        return score
    
    
        # ---------------------------------- #
    # Top K Context
    # ---------------------------------- #

    def top_k(
        self,
        contexts: list[str],
        query: str,
        k: int
    ) -> list[str]:
        """
        Return top-k
        ranked context.
        """

        self.logger.info(
            f"Selecting top {k} context items."
        )

        return self.rank(
            contexts,
            query
        )[:k]

    # ---------------------------------- #
    # Rank Metadata
    # ---------------------------------- #

    def rank_metadata(
        self,
        metadata: dict,
        query: str
    ) -> dict:
        """
        Rank metadata
        by relevance.
        """

        ranked = {}

        query = (
            query.lower()
        )

        for key, value in metadata.items():

            text = (
                str(value)
                .lower()
            )

            score = 0

            for word in query.split():

                if word in text:

                    score += 1

            ranked[key] = {

                "score": score,

                "value": value,

            }

        return dict(

            sorted(

                ranked.items(),

                key=lambda item:

                item[1]["score"],

                reverse=True,

            )

        )

    # ---------------------------------- #
    # Filter Empty Context
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
    # Ranking Statistics
    # ---------------------------------- #

    def statistics(
        self,
        contexts: list[str]
    ) -> dict:
        """
        Return ranking
        statistics.
        """

        return {

            "total_context":
            len(
                contexts
            ),

            "non_empty":
            len(
                self.remove_empty(
                    contexts
                )
            ),

        }

    # ---------------------------------- #
    # Context Exists
    # ---------------------------------- #

    def contains(
        self,
        contexts: list[str],
        context: str
    ) -> bool:
        """
        Check whether a
        context item
        exists.
        """

        return (
            context
            in contexts
        )

    # ---------------------------------- #
    # Clear Ranker
    # ---------------------------------- #

    def clear(
        self
    ) -> None:
        """
        Reset Context
        Ranker.
        """

        self.logger.info(
            "Context Ranker reset."
        )
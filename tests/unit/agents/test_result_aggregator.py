"""
File: tests/unit/agents/test_result_aggregator.py

Purpose:
Unit tests for ResultAggregator.
"""

from core.agents.result_aggregator import (
    ResultAggregator
)


def test_aggregator_creation():
    """
    Verify aggregator initialization.
    """

    aggregator = ResultAggregator()

    assert aggregator is not None


def test_aggregate_results():
    """
    Verify result aggregation.
    """

    aggregator = ResultAggregator()

    results = [
        "architecture",
        "security",
        "research"
    ]

    aggregated = (
        aggregator.aggregate(
            results
        )
    )

    assert aggregated == results


def test_result_count():
    """
    Verify result counting.
    """

    aggregator = ResultAggregator()

    results = [
        "one",
        "two",
        "three"
    ]

    assert (
        aggregator.count(
            results
        )
        == 3
    )


def test_empty_results():
    """
    Verify empty aggregation.
    """

    aggregator = ResultAggregator()

    results = []

    aggregated = (
        aggregator.aggregate(
            results
        )
    )

    assert aggregated == []


def test_single_result():
    """
    Verify single result.
    """

    aggregator = ResultAggregator()

    results = [
        "architecture"
    ]

    aggregated = (
        aggregator.aggregate(
            results
        )
    )

    assert aggregated == results
"""
File: tests/unit/context/test_context_compressor.py

Purpose:
Unit tests for ContextCompressor.
"""

from core.context.context_compressor import (
    ContextCompressor
)


def test_compressor_creation():
    """
    Verify initialization.
    """

    compressor = ContextCompressor()

    assert compressor is not None


def test_context_compression():
    """
    Verify compression.
    """

    compressor = ContextCompressor()

    contexts = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F"
    ]

    result = compressor.compress(
        contexts,
        max_items=3
    )

    assert len(result) == 3


def test_small_context():
    """
    Verify small context handling.
    """

    compressor = ContextCompressor()

    contexts = [
        "A",
        "B"
    ]

    result = compressor.compress(
        contexts,
        max_items=5
    )

    assert len(result) == 2


def test_compression_ratio():
    """
    Verify ratio calculation.
    """

    compressor = ContextCompressor()

    ratio = (
        compressor.compression_ratio(
            10,
            5
        )
    )

    assert ratio == 0.5


def test_empty_ratio():
    """
    Verify zero division handling.
    """

    compressor = ContextCompressor()

    ratio = (
        compressor.compression_ratio(
            0,
            0
        )
    )

    assert ratio == 0.0
"""
File:
tests/unit/orchestration/
test_error_analyzer.py

Purpose:
Verify error analysis.
"""

from core.orchestration.error_analyzer import (
    ErrorAnalyzer
)


def test_import_error():
    """
    Verify import analysis.
    """

    analyzer = (
        ErrorAnalyzer()
    )

    result = analyzer.analyze(
        "ImportError"
    )

    assert (
        result["error_type"]
        == "ImportError"
    )


def test_syntax_error():
    """
    Verify syntax analysis.
    """

    analyzer = (
        ErrorAnalyzer()
    )

    result = analyzer.analyze(
        "SyntaxError"
    )

    assert (
        result["severity"]
        == "high"
    )


def test_name_error():
    """
    Verify name analysis.
    """

    analyzer = (
        ErrorAnalyzer()
    )

    result = analyzer.analyze(
        "NameError"
    )

    assert (
        result["error_type"]
        == "NameError"
    )


def test_unknown_error():
    """
    Verify fallback.
    """

    analyzer = (
        ErrorAnalyzer()
    )

    result = analyzer.analyze(
        "Random Failure"
    )

    assert (
        result["error_type"]
        == "UnknownError"
    )
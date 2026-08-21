"""
File:
tests/unit/orchestration/
test_self_correction.py

Purpose:
Verify self correction.
"""

from core.orchestration.self_correction import (
    SelfCorrection
)


def test_import_fix():
    """
    Verify dependency repair.
    """

    correction = (
        SelfCorrection()
    )

    result = (
        correction.generate_fix(
            {
                "error_type":
                "ImportError"
            }
        )
    )

    assert (
        result["action"]
        == "InstallDependency"
    )


def test_syntax_fix():
    """
    Verify syntax repair.
    """

    correction = (
        SelfCorrection()
    )

    result = (
        correction.generate_fix(
            {
                "error_type":
                "SyntaxError"
            }
        )
    )

    assert (
        result["target"]
        == "CoderAgent"
    )


def test_name_fix():
    """
    Verify name repair.
    """

    correction = (
        SelfCorrection()
    )

    result = (
        correction.generate_fix(
            {
                "error_type":
                "NameError"
            }
        )
    )

    assert (
        result["action"]
        == "DefineMissingName"
    )


def test_unknown_fix():
    """
    Verify fallback repair.
    """

    correction = (
        SelfCorrection()
    )

    result = (
        correction.generate_fix(
            {
                "error_type":
                "UnknownError"
            }
        )
    )

    assert (
        result["action"]
        == "ManualInvestigation"
    )
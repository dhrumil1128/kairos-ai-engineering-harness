"""
File:
tests/unit/cli/test_prompt.py

Purpose:
Verify CLI prompt.
"""

from core.cli.prompt import (
    Prompt
)


def test_prompt_creation():
    """
    Verify creation.
    """

    prompt = Prompt()

    assert prompt is not None


def test_prompt_text():
    """
    Verify prompt value.
    """

    prompt = Prompt()

    assert (
        prompt.get_prompt()
        == "kairos > "
    )


def test_prompt_exists():
    """
    Verify getter exists.
    """

    prompt = Prompt()

    assert hasattr(
        prompt,
        "get_prompt"
    )


def test_input_method_exists():
    """
    Verify input method.
    """

    prompt = Prompt()

    assert hasattr(
        prompt,
        "get_input"
    )
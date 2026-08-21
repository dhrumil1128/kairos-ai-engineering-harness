"""
File: tests/unit/context/test_context_loader.py

Purpose:
Unit tests for ContextLoader.
"""

from pathlib import Path

from core.context.context_loader import (
    ContextLoader
)


def test_loader_creation():
    """
    Verify initialization.
    """

    loader = ContextLoader()

    assert loader is not None


def test_missing_file():
    """
    Verify missing file handling.
    """

    loader = ContextLoader()

    result = loader.load_file(
        "missing_file.md"
    )

    assert result == ""


def test_file_exists():
    """
    Verify existence check.
    """

    temp_file = (
        Path("temp_test.md")
    )

    temp_file.write_text(
        "hello",
        encoding="utf-8"
    )

    loader = ContextLoader()

    assert (
        loader.file_exists(
            "temp_test.md"
        )
        is True
    )

    temp_file.unlink()


def test_load_file():
    """
    Verify file loading.
    """

    temp_file = (
        Path("temp_test.md")
    )

    temp_file.write_text(
        "hello world",
        encoding="utf-8"
    )

    loader = ContextLoader()

    content = loader.load_file(
        "temp_test.md"
    )

    assert (
        content
        == "hello world"
    )

    temp_file.unlink()


def test_nonexistent_file():
    """
    Verify missing existence check.
    """

    loader = ContextLoader()

    assert (
        loader.file_exists(
            "does_not_exist.md"
        )
        is False
    )
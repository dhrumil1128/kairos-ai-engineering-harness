"""
File: tests/unit/context/test_project_loader.py

Purpose:
Unit tests for ProjectLoader.
"""

from pathlib import Path

from core.context.project_loader import (
    ProjectLoader
)


def test_loader_creation():
    """
    Verify initialization.
    """

    loader = ProjectLoader()

    assert loader is not None


def test_expected_files():
    """
    Verify supported files.
    """

    loader = ProjectLoader()

    assert (
        "README.md"
        in loader.expected_files()
    )


def test_load_empty_project():
    """
    Verify empty project load.
    """

    loader = ProjectLoader()

    result = loader.load_project(
        "."
    )

    assert isinstance(
        result,
        dict
    )


def test_load_single_file():
    """
    Verify file loading.
    """

    file_path = Path(
        "README.md"
    )

    file_path.write_text(
        "Project Test",
        encoding="utf-8"
    )

    loader = ProjectLoader()

    result = loader.load_project(
        "."
    )

    assert (
        result["README.md"]
        == "Project Test"
    )

    file_path.unlink()


def test_file_count():
    """
    Verify enterprise file list.
    """

    loader = ProjectLoader()

    assert (
        len(
            loader.expected_files()
        )
        == 11
    )
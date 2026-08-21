"""
File:
tests/unit/tools/
test_file_tool.py

Purpose:
Unit tests for FileTool.
"""

from core.tools.file_tool import (
    FileTool
)


def test_write_and_read_file(
    tmp_path
):
    """
    Verify write/read.
    """

    tool = FileTool()

    test_file = (
        tmp_path
        / "test.txt"
    )

    tool.write_file(
        str(test_file),
        "KAIROS"
    )

    result = tool.read_file(
        str(test_file)
    )

    assert result == "KAIROS"


def test_exists_true(
    tmp_path
):
    """
    Verify existence.
    """

    tool = FileTool()

    test_file = (
        tmp_path
        / "exists.txt"
    )

    tool.write_file(
        str(test_file),
        "data"
    )

    assert (
        tool.exists(
            str(test_file)
        )
        is True
    )


def test_exists_false(
    tmp_path
):
    """
    Verify missing file.
    """

    tool = FileTool()

    test_file = (
        tmp_path
        / "missing.txt"
    )

    assert (
        tool.exists(
            str(test_file)
        )
        is False
    )


def test_delete_file(
    tmp_path
):
    """
    Verify deletion.
    """

    tool = FileTool()

    test_file = (
        tmp_path
        / "delete.txt"
    )

    tool.write_file(
        str(test_file),
        "temp"
    )

    tool.delete_file(
        str(test_file)
    )

    assert (
        tool.exists(
            str(test_file)
        )
        is False
    )
    
def test_create_directory(
    tmp_path
):

    tool = FileTool()

    path = (
        tmp_path
        / "test_dir"
    )

    tool.create_directory(
        str(path)
    )

    assert (
        path.exists()
    )


def test_resolve_path_keeps_absolute_windows_path():

    tool = FileTool()

    assert (
        str(tool.resolve_path("D:\\Jarvis"))
        == "D:\\Jarvis"
    )


def test_resolve_path_unwraps_workspace_prefixed_absolute_windows_path():

    tool = FileTool()

    assert (
        str(tool.resolve_path("workspace/D:\\Jarvis"))
        == "D:\\Jarvis"
    )


def test_resolve_path_scopes_relative_path_to_workspace():

    tool = FileTool()

    assert (
        str(tool.resolve_path("docs"))
        == str(tool.WORKSPACE_ROOT / "docs")
    )

def test_list_directory(
    tmp_path
):

    tool = FileTool()

    file_path = (
        tmp_path
        / "sample.txt"
    )

    file_path.write_text(
        "hello"
    )

    result = (
        tool.list_directory(
            str(tmp_path)
        )
    )

    assert (
        "sample.txt"
        in result
    )
    
    
def test_create_kairos_project(
    tmp_path
):

    tool = FileTool()

    tool.create_kairos_project(
        str(tmp_path)
    )

    kairos_dir = (
        tmp_path
        / ".kairos"
    )

    assert (
        kairos_dir.exists()
    )

    assert (
        kairos_dir
        / "architecture.md"
    ).exists()

    assert (
        kairos_dir
        / "roadmap.md"
    ).exists()

    assert (
        kairos_dir
        / "coding_standards.md"
    ).exists()

    assert (
        kairos_dir
        / "project_context.md"
    ).exists()

    assert (
        kairos_dir
        / "memory.md"
    ).exists()

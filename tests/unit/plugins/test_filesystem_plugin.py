"""
File:
tests/unit/plugins/
test_filesystem_plugin.py

Purpose:
Verify FilesystemPlugin.
"""

import pytest

from core.plugins.filesystem_plugin import (
    FilesystemPlugin
)


def test_plugin_name():
    """
    Verify plugin name.
    """

    plugin = FilesystemPlugin()

    assert (
        plugin.name
        == "FilesystemPlugin"
    )


def test_write_and_read(
    tmp_path
):
    """
    Verify file operations.
    """

    plugin = FilesystemPlugin()

    test_file = (
        tmp_path
        / "test.txt"
    )

    plugin.execute(
        "write",
        str(test_file),
        "KAIROS"
    )

    result = plugin.execute(
        "read",
        str(test_file)
    )

    assert result == "KAIROS"


def test_exists(
    tmp_path
):
    """
    Verify existence.
    """

    plugin = FilesystemPlugin()

    test_file = (
        tmp_path
        / "exists.txt"
    )

    plugin.execute(
        "write",
        str(test_file),
        "data"
    )

    assert (
        plugin.execute(
            "exists",
            str(test_file)
        )
        is True
    )


def test_delete(
    tmp_path
):
    """
    Verify deletion.
    """

    plugin = FilesystemPlugin()

    test_file = (
        tmp_path
        / "delete.txt"
    )

    plugin.execute(
        "write",
        str(test_file),
        "temp"
    )

    plugin.execute(
        "delete",
        str(test_file)
    )

    assert (
        plugin.execute(
            "exists",
            str(test_file)
        )
        is False
    )


def test_invalid_action():
    """
    Verify validation.
    """

    plugin = FilesystemPlugin()

    with pytest.raises(
        ValueError
    ):
        plugin.execute(
            "invalid_action"
        )


def test_create_directory_action(
    tmp_path
):

    plugin = (
        FilesystemPlugin()
    )

    path = (
        tmp_path
        / "test_dir"
    )

    result = (
        plugin.execute(
            "create_directory",
            str(path)
        )
    )

    assert result is True

    assert (
        path.exists()
    )


def test_list_directory_action(
    tmp_path
):

    plugin = (
        FilesystemPlugin()
    )

    (
        tmp_path
        / "sample.txt"
    ).write_text(
        "hello"
    )

    result = (
        plugin.execute(
            "list_directory",
            str(tmp_path)
        )
    )

    assert (
        "sample.txt"
        in result
    )
    
    
def test_init_project_action(
    tmp_path
):
    """
    Verify KAIROS project creation.
    """

    plugin = (
        FilesystemPlugin()
    )

    result = (
        plugin.execute(
            "init_project",
            str(tmp_path)
        )
    )

    assert result is True

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
    
    
    
    

def test_exists_false(
    tmp_path
):

    plugin = (
        FilesystemPlugin()
    )

    test_file = (
        tmp_path
        / "missing.txt"
    )

    assert (
        plugin.execute(
            "exists",
            str(test_file)
        )
        is False
    )
    

def test_list_directory_empty(
    tmp_path
):

    plugin = (
        FilesystemPlugin()
    )

    result = (
        plugin.execute(
            "list_directory",
            str(tmp_path)
        )
    )

    assert result == []
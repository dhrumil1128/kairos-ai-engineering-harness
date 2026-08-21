"""
File:
tests/unit/cli/test_cli_manager.py

Purpose:
Verify CLI manager.
"""
import pytest
from core.cli.cli_manager import (
    CLIManager
)


def test_creation():
    """
    Verify creation.
    """

    manager = CLIManager()

    assert manager is not None


def test_help_command():
    """
    Verify help.
    """

    manager = CLIManager()

    result = (
        manager.process_command(
            "/help"
        )
    )

    assert (
        result["status"]
        == "success"
    )


def test_status_command():
    """
    Verify status.
    """

    manager = CLIManager()

    result = (
        manager.process_command(
            "/status"
        )
    )

    assert (
        result["message"]
        == "KAIROS Active"
    )

@pytest.mark.skip(
    reason="Requires live Gemini API"
)
def test_default_command():
    """
    Verify normal command.
    """

    manager = CLIManager()

    result = (
        manager.process_command(
            "build api"
        )
    )

    assert (
    result["status"]
    == "completed"
)
    
@pytest.mark.skip(
    reason="Requires live Gemini API"
)  
def test_agent_pipeline():
    """
    Verify full pipeline.
    """

    manager = CLIManager()

    result = (
        manager.process_command(
            "build auth api"
        )
    )

    assert (
        result["status"]
        == "completed"
    )
    



def test_mcps_command():

    manager = CLIManager()

    result = (
        manager.process_command(
            "/mcps"
        )
    )

    assert (
        result["status"]
        == "success"
    )


def test_plugins_command():

    manager = CLIManager()

    result = (
        manager.process_command(
            "/plugins"
        )
    )

    assert (
        result["status"]
        == "success"
    )


def test_tools_command():

    manager = CLIManager()

    result = (
        manager.process_command(
            "/tools"
        )
    )

    assert (
        result["status"]
        == "success"
    )


def test_init_project_command(
    tmp_path
):

    manager = (
        CLIManager()
    )

    result = (
        manager.process_command(
            f"/init-project {tmp_path}"
        )
    )

    assert (
        result["status"]
        == "success"
    )

    assert (
        tmp_path
        / ".kairos"
    ).exists()
    
    


def test_create_dir_command(
    tmp_path
):

    manager = (
        CLIManager()
    )

    path = (
        tmp_path
        / "src"
    )

    result = (
        manager.process_command(
            f"/create-dir {path}"
        )
    )

    assert (
        result["status"]
        == "success"
    )

    assert path.exists()
    
    

def test_list_files_command(
    tmp_path
):

    manager = (
        CLIManager()
    )

    (
        tmp_path
        / "sample.txt"
    ).write_text(
        "hello"
    )

    result = (
        manager.process_command(
            f"/list-files {tmp_path}"
        )
    )

    assert (
        result["status"]
        == "success"
    )

    assert (
        "sample.txt"
        in result["files"]
    )


def test_read_file_command(
    tmp_path
):

    manager = (
        CLIManager()
    )

    file_path = (
        tmp_path
        / "test.txt"
    )

    file_path.write_text(
        "hello",
        encoding="utf-8"
    )

    result = (
        manager.process_command(
            f"/read-file {file_path}"
        )
    )

    assert (
        result["status"]
        == "success"
    )

    assert (
        result["message"]
        == "hello"
    )
    
    
def test_write_file_command(
    tmp_path
):

    manager = (
        CLIManager()
    )

    file_path = (
        tmp_path
        / "output.txt"
    )

    result = (
        manager.process_command(
            f"/write-file {file_path}|hello"
        )
    )

    assert (
        result["status"]
        == "success"
    )

    assert (
        file_path.exists()
    )

    assert (
        file_path.read_text(
            encoding="utf-8"
        )
        == "hello"
    )
    

def test_exists_file_command(
    tmp_path
):

    manager = (
        CLIManager()
    )

    file_path = (
        tmp_path
        / "exists.txt"
    )

    file_path.write_text(
        "hello"
    )

    result = (
        manager.process_command(
            f"/exists-file {file_path}"
        )
    )

    assert (
        result["status"]
        == "success"
    )

    assert (
        result["message"]
        == "True"
    )
    
    
    
def test_delete_file_command(
    tmp_path
):

    manager = (
        CLIManager()
    )

    file_path = (
        tmp_path
        / "delete_me.txt"
    )

    file_path.write_text(
        "hello"
    )

    result = (
        manager.process_command(
            f"/delete-file {file_path}"
        )
    )

    assert (
        result["status"]
        == "success"
    )

    assert (
        not file_path.exists()
    )
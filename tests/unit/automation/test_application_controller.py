"""
File:
tests/unit/automation/
test_application_controller.py

Purpose:
Verify real application controller.
"""

import pytest
from unittest.mock import patch

from core.automation.application_controller import (
    ApplicationController
)


def test_controller_creation():
    """
    Verify creation.
    """

    controller = (
        ApplicationController()
    )

    assert controller is not None


def test_allowed_application():
    """
    Verify allowed app.
    """

    controller = (
        ApplicationController()
    )

    with patch('subprocess.Popen') as mock_popen:
        mock_popen.return_value.pid = 1234
        result = controller.launch(
            
            "Code"
        )

    assert "Launched:" in result

def test_blocked_application():
    """
    Verify blocked app.
    """

    controller = (
        ApplicationController()
    )

    with pytest.raises(
        PermissionError
    ):
        controller.launch(
            "malware.exe"
        )


def test_process_listing():
    """
    Verify process retrieval.
    """

    controller = (
        ApplicationController()
    )

    processes = (
        controller.list_processes()
    )

    assert isinstance(
        processes,
        list
    )
    
    
def test_launch_exists():
    controller = ApplicationController()

    assert hasattr(
        controller,
        "launch"
    )
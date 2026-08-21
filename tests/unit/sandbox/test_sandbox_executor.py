"""
File: tests/unit/sandbox/test_sandbox_executor.py

Purpose:
Unit tests for SandboxExecutor web-server and CLI execution paths.

Tests cover all five validation scenarios described in the
KAIROS sandbox execution specification:

  Test 1 — CLI Python script (print / exit-0)
  Test 2 — Flask application startup + graceful shutdown
  Test 3 — FastAPI application startup + graceful shutdown
  Test 4 — Runtime exception during startup (non-zero exit)
  Test 5 — Packaged PyInstaller executable (sys.frozen)

Architecture:

SandboxExecutor
     ↓
_execute_cli  /  _execute_web_server
     ↓
SandboxResult
"""

from __future__ import annotations

import subprocess
import sys
from io import StringIO
from types import SimpleNamespace
from unittest.mock import MagicMock, patch, PropertyMock

import pytest

from core.sandbox.sandbox_executor import SandboxExecutor
from core.sandbox.sandbox_result import SandboxResult


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_meta(
    commands: list[list[str]],
    is_web_server: bool = False,
) -> dict:
    """Build a minimal execution metadata dict."""
    return {
        "runtime": "python",
        "entrypoint": "src/main.py",
        "commands": commands,
        "is_web_server": is_web_server,
    }


def _completed_process(returncode: int = 0, stdout: str = "", stderr: str = "") -> subprocess.CompletedProcess:
    """Build a fake subprocess.CompletedProcess."""
    cp = subprocess.CompletedProcess(args=[], returncode=returncode)
    cp.stdout = stdout
    cp.stderr = stderr
    return cp


# ---------------------------------------------------------------------------
# Test 1 — CLI Python script
# ---------------------------------------------------------------------------

class TestCLIExecution:
    """SandboxExecutor._execute_cli() produces correct SandboxResult."""

    def _executor_with_entrypoint(self, tmp_path):
        """Create an executor whose entrypoint exists."""
        # Create the required src/main.py so the executor
        # does not short-circuit with 'Entrypoint not found'.
        (tmp_path / "src").mkdir(parents=True, exist_ok=True)
        (tmp_path / "src" / "main.py").write_text('print("Hello")\n')
        executor = SandboxExecutor()
        return executor, str(tmp_path)

    def test_cli_success_returns_success_result(self, tmp_path):
        """
        Test 1: Single Python script — print("Hello").
        subprocess.run returns exit code 0 → SandboxResult.success == True.
        """
        executor, project_path = self._executor_with_entrypoint(tmp_path)

        meta = _make_meta([["python", "src/main.py"]], is_web_server=False)

        completed = _completed_process(returncode=0, stdout="Hello\n", stderr="")

        with (
            patch.object(executor.command_resolver, "resolve", return_value=meta),
            patch("subprocess.run", return_value=completed) as mock_run,
        ):
            result = executor.execute(project_path)

        assert isinstance(result, SandboxResult)
        assert result.success is True
        assert result.exit_code == 0
        assert "Hello" in result.stdout
        mock_run.assert_called_once()

    def test_cli_failure_returns_failure_result(self, tmp_path):
        """
        CLI script exits with non-zero → SandboxResult.success == False.
        """
        executor, project_path = self._executor_with_entrypoint(tmp_path)

        meta = _make_meta([["python", "src/main.py"]], is_web_server=False)
        completed = _completed_process(returncode=1, stdout="", stderr="ZeroDivisionError")

        with (
            patch.object(executor.command_resolver, "resolve", return_value=meta),
            patch("subprocess.run", return_value=completed),
        ):
            result = executor.execute(project_path)

        assert result.success is False
        assert result.exit_code == 1
        assert "ZeroDivisionError" in result.stderr

    def test_cli_timeout_returns_failure(self, tmp_path):
        """
        TimeoutExpired is caught and returned as failure (exit_code=-2).
        """
        executor, project_path = self._executor_with_entrypoint(tmp_path)

        meta = _make_meta([["python", "src/main.py"]], is_web_server=False)

        with (
            patch.object(executor.command_resolver, "resolve", return_value=meta),
            patch("subprocess.run", side_effect=subprocess.TimeoutExpired(cmd=[], timeout=30)),
        ):
            result = executor.execute(project_path)

        assert result.success is False
        assert result.exit_code == -2

    def test_missing_entrypoint_returns_failure(self, tmp_path):
        """
        Missing src/main.py → SandboxResult.success == False, no subprocess call.
        """
        executor = SandboxExecutor()
        project_path = str(tmp_path)  # No src/main.py created.

        with patch("subprocess.run") as mock_run:
            result = executor.execute(project_path)

        assert result.success is False
        assert result.exit_code == -1
        mock_run.assert_not_called()


# ---------------------------------------------------------------------------
# Test 2 — Flask application
# Test 3 — FastAPI application
# ---------------------------------------------------------------------------

class TestWebServerExecution:
    """
    SandboxExecutor._execute_web_server() launches Popen,
    waits, verifies liveness, terminates, and returns success.
    """

    def _executor_with_entrypoint(self, tmp_path, framework: str = "flask"):
        (tmp_path / "src").mkdir(parents=True, exist_ok=True)
        source = f"import {framework}\napp = {framework}.Flask(__name__)\n"
        (tmp_path / "src" / "main.py").write_text(source)
        executor = SandboxExecutor()
        return executor, str(tmp_path)

    def _make_alive_popen(self, stdout="", stderr=""):
        """
        Return a mock Popen where poll() → None (process alive)
        and communicate() returns captured output.
        """
        mock_proc = MagicMock(spec=subprocess.Popen)
        mock_proc.pid = 12345
        mock_proc.poll.return_value = None          # still alive
        mock_proc.communicate.return_value = (stdout, stderr)
        mock_proc.wait.return_value = 0
        return mock_proc

    def _test_web_server_success(self, tmp_path, framework: str):
        executor, project_path = self._executor_with_entrypoint(tmp_path, framework)

        meta = _make_meta(
            [["python", "src/main.py"]],
            is_web_server=True,
        )

        mock_proc = self._make_alive_popen(
            stdout=f" * Running on http://127.0.0.1:5000\n",
            stderr="",
        )

        with (
            patch.object(executor.command_resolver, "resolve", return_value=meta),
            patch("subprocess.Popen", return_value=mock_proc),
            patch("time.sleep"),  # Skip real sleep in tests.
            patch.object(
                executor,
                "_probe_web_server",
                return_value=(True, 5000),
            ),
        ):
            result = executor.execute(project_path)

        assert isinstance(result, SandboxResult)
        assert result.success is True
        assert result.exit_code == 0
        # Server must have been terminated.
        mock_proc.terminate.assert_called_once()

    def test_flask_server_returns_success(self, tmp_path):
        """Test 2: Flask application → sandbox returns success."""
        self._test_web_server_success(tmp_path, framework="flask")

    def test_fastapi_server_returns_success(self, tmp_path):
        """Test 3: FastAPI application → sandbox returns success."""
        self._test_web_server_success(tmp_path, framework="fastapi")

    def test_web_server_terminated_after_sandbox(self, tmp_path):
        """
        Server process must always be terminated,
        even when the HTTP probe succeeds.
        """
        executor, project_path = self._executor_with_entrypoint(tmp_path)

        meta = _make_meta([["python", "src/main.py"]], is_web_server=True)
        mock_proc = self._make_alive_popen()

        with (
            patch.object(executor.command_resolver, "resolve", return_value=meta),
            patch("subprocess.Popen", return_value=mock_proc),
            patch("time.sleep"),
            patch.object(executor, "_probe_web_server", return_value=(True, 5000)),
        ):
            executor.execute(project_path)

        mock_proc.terminate.assert_called_once()

    def test_web_server_success_without_http_probe(self, tmp_path):
        """
        If the HTTP probe fails but the process is still alive,
        the sandbox still returns success (process liveness is primary signal).
        """
        executor, project_path = self._executor_with_entrypoint(tmp_path)

        meta = _make_meta([["python", "src/main.py"]], is_web_server=True)
        mock_proc = self._make_alive_popen()

        with (
            patch.object(executor.command_resolver, "resolve", return_value=meta),
            patch("subprocess.Popen", return_value=mock_proc),
            patch("time.sleep"),
            patch.object(executor, "_probe_web_server", return_value=(False, None)),
        ):
            result = executor.execute(project_path)

        assert result.success is True


# ---------------------------------------------------------------------------
# Test 4 — Runtime exception during startup
# ---------------------------------------------------------------------------

class TestWebServerStartupFailure:
    """
    When a web server exits before the probe window,
    SandboxExecutor returns failure with captured stderr.
    """

    def test_startup_crash_returns_failure(self, tmp_path):
        """
        Test 4: Server exits immediately (import error / exception)
        → sandbox returns failure with captured stderr.
        """
        (tmp_path / "src").mkdir(parents=True, exist_ok=True)
        (tmp_path / "src" / "main.py").write_text(
            "import flask\nraise RuntimeError('boom')\n"
        )
        executor = SandboxExecutor()
        project_path = str(tmp_path)

        meta = _make_meta([["python", "src/main.py"]], is_web_server=True)

        mock_proc = MagicMock(spec=subprocess.Popen)
        mock_proc.pid = 9999
        # poll() returns non-None → process exited prematurely.
        mock_proc.poll.return_value = 1
        mock_proc.communicate.return_value = ("", "RuntimeError: boom\n")

        with (
            patch.object(executor.command_resolver, "resolve", return_value=meta),
            patch("subprocess.Popen", return_value=mock_proc),
            patch("time.sleep"),
        ):
            result = executor.execute(project_path)

        assert result.success is False
        assert result.exit_code == 1
        assert "boom" in result.stderr


# ---------------------------------------------------------------------------
# Test 5 — Packaged PyInstaller executable
# ---------------------------------------------------------------------------

class TestPyInstallerExecution:
    """
    When running inside a frozen PyInstaller build,
    ExecutionCommandResolver._resolve_python_executable()
    must return a real Python interpreter from PATH.
    """

    def test_frozen_build_uses_path_python(self):
        """
        Test 5: sys.frozen is True → resolver falls back to shutil.which("python").
        """
        from core.sandbox.execution_command_resolver import ExecutionCommandResolver

        resolver = ExecutionCommandResolver()

        with (
            patch.object(sys, "frozen", True, create=True),
            patch("shutil.which", return_value="/usr/bin/python"),
        ):
            python_exe = resolver._resolve_python_executable()

        assert python_exe == "/usr/bin/python"

    def test_frozen_build_raises_when_no_python(self):
        """
        If no Python interpreter is found on PATH in a frozen build,
        a RuntimeError is raised.
        """
        from core.sandbox.execution_command_resolver import ExecutionCommandResolver

        resolver = ExecutionCommandResolver()

        with (
            patch.object(sys, "frozen", True, create=True),
            patch("shutil.which", return_value=None),
        ):
            with pytest.raises(RuntimeError, match="Python interpreter not found"):
                resolver._resolve_python_executable()


# ---------------------------------------------------------------------------
# ExecutionCommandResolver — web server detection
# ---------------------------------------------------------------------------

class TestWebServerDetection:
    """
    ExecutionCommandResolver._is_web_server() detects
    web frameworks via metadata and source scanning.
    """

    def test_flask_detected_via_metadata(self, tmp_path):
        from core.sandbox.execution_command_resolver import ExecutionCommandResolver

        resolver = ExecutionCommandResolver()
        result = resolver._is_web_server(
            framework="flask",
            project_path=tmp_path,
            entry_point="src/main.py",
        )
        assert result is True

    def test_fastapi_detected_via_metadata(self, tmp_path):
        from core.sandbox.execution_command_resolver import ExecutionCommandResolver

        resolver = ExecutionCommandResolver()
        result = resolver._is_web_server(
            framework="fastapi",
            project_path=tmp_path,
            entry_point="src/main.py",
        )
        assert result is True

    def test_django_detected_via_metadata(self, tmp_path):
        from core.sandbox.execution_command_resolver import ExecutionCommandResolver

        resolver = ExecutionCommandResolver()
        result = resolver._is_web_server(
            framework="django",
            project_path=tmp_path,
            entry_point="src/main.py",
        )
        assert result is True

    def test_cli_not_detected_as_web_server(self, tmp_path):
        from core.sandbox.execution_command_resolver import ExecutionCommandResolver

        resolver = ExecutionCommandResolver()
        result = resolver._is_web_server(
            framework="",
            project_path=tmp_path,
            entry_point="src/main.py",
        )
        assert result is False

    def test_flask_detected_via_source_scan(self, tmp_path):
        """
        When framework metadata is absent, detection falls
        back to scanning the entrypoint source for imports.
        """
        from core.sandbox.execution_command_resolver import ExecutionCommandResolver

        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.py").write_text(
            "from flask import Flask\napp = Flask(__name__)\n"
        )

        resolver = ExecutionCommandResolver()
        result = resolver._is_web_server(
            framework="",           # No metadata.
            project_path=tmp_path,
            entry_point="src/main.py",
        )
        assert result is True

    def test_fastapi_detected_via_source_scan(self, tmp_path):
        from core.sandbox.execution_command_resolver import ExecutionCommandResolver

        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.py").write_text(
            "import fastapi\napp = fastapi.FastAPI()\n"
        )

        resolver = ExecutionCommandResolver()
        result = resolver._is_web_server(
            framework="",
            project_path=tmp_path,
            entry_point="src/main.py",
        )
        assert result is True

    def test_plain_script_not_detected_as_web_server(self, tmp_path):
        from core.sandbox.execution_command_resolver import ExecutionCommandResolver

        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.py").write_text(
            'print("Hello, World!")\n'
        )

        resolver = ExecutionCommandResolver()
        result = resolver._is_web_server(
            framework="",
            project_path=tmp_path,
            entry_point="src/main.py",
        )
        assert result is False

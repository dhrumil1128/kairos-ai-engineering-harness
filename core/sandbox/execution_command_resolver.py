"""
File: core/sandbox/execution_command_resolver.py

Purpose:
Resolve the correct execution command for a generated project.

This class DOES NOT execute anything.
It only returns the command that SandboxExecutor
should run.
"""

from pathlib import Path
from typing import Any
import shutil
import sys

class ExecutionCommandResolver:
    """
    Resolve execution commands for generated projects.
    """

    def _resolve_python_executable(self) -> str:
        """
        Resolve the Python binary path.
        
        If running inside a frozen PyInstaller application, sys.executable points to
        the main KAIROS binary instead of Python. Fall back to finding Python on PATH.
        """
        if getattr(sys, "frozen", False):
            python_path = shutil.which("python") or shutil.which("python3")
            if not python_path:
                raise RuntimeError("Python interpreter not found on PATH for frozen build.")
            return python_path
        return sys.executable

    def resolve(
        self,
        project_path: str,
        architecture: dict | None = None,
    ) -> dict[str, Any] | None:
        """
        Resolve the execution command.

        Parameters
        ----------
        project_path:
            Generated project path.

        architecture:
            Architecture metadata produced by KAIROS.
            (Optional in V1.)

        Returns
        -------
        dict[str, Any] | None
            Execution metadata including runtime, entrypoint, and commands.
        """

        # Safe defaults
        language = "python"
        framework = ""
        entry_point = "src/main.py"

        # Use architecture when available
        if architecture:
            getter = (
                architecture.get
                if hasattr(architecture, "get")
                else lambda key, default=None: getattr(
                    architecture,
                    key,
                    default,
                )
            )
            language = (getter("language", language) or language).lower()
            framework = (getter("framework", framework) or "").lower()
            entry_point = getter("entry_point", entry_point)

        root = Path(project_path)

        if not (root / str(Path(entry_point))).exists():
            root_python_files = [
                file
                for file in root.glob("*.py")
                if file.is_file()
            ]

            if len(root_python_files) == 1:
                entry_point = root_python_files[0].name

        # Absolute entrypoint
        entry = str(Path(entry_point))

        python_exe = self._resolve_python_executable()

        # -----------------------------
        # Python
        # -----------------------------
        if language == "python":

            if framework in ("click", "typer"):
                return {
                    "runtime": "python",
                    "entrypoint": entry,
                    "commands": [
                        [python_exe, entry, "--help"]
                    ]
                }

            # Generic Python application
            return {
                "runtime": "python",
                "entrypoint": entry,
                "commands": [
                    [python_exe, entry]
                ]
            }

        # -----------------------------
        # Future languages
        # -----------------------------
        return {
            "runtime": "python",
            "entrypoint": entry,
            "commands": [
                [python_exe, entry]
            ]
        }


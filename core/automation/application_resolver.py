"""
Resolve desktop application executables.

Purpose
-------
Find the executable for a requested
desktop application without hardcoded
installation paths.

Resolution order
----------------
1. Windows PATH
2. Running processes
3. Raise FileNotFoundError

Future
------
V2:
- Windows App Paths Registry

V3:
- Start Menu shortcuts

V4:
- Windows Package Manager
"""

from __future__ import annotations
import winreg
import shutil
from pathlib import Path

import psutil


class ApplicationResolver:
    """
    Resolve application executables.
    """

    
    def _resolve_from_registry(
        self,
        application: str,
    ) -> str | None:
        """
        Resolve an application from the
        Windows App Paths registry.
        """

        executable = application

        if not executable.lower().endswith(".exe"):
            executable += ".exe"

        registry_locations = (
            (
                winreg.HKEY_LOCAL_MACHINE,
                rf"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\{executable}",
            ),
            (
                winreg.HKEY_CURRENT_USER,
                rf"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\{executable}",
            ),
        )

        for root, subkey in registry_locations:

            try:
                with winreg.OpenKey(root, subkey) as key:

                    path, _ = winreg.QueryValueEx(
                        key,
                        None,
                    )

                    if Path(path).exists():
                        return path

            except FileNotFoundError:
                continue

        return None
        
        
    def resolve(
        self,
        application: str,
        ) -> str:
        """
        Resolve an executable path.
        """

        if not application:
            raise ValueError(
                "Application name cannot be empty."
            )

        application = application.strip()

        # ----------------------------------
        # PATH lookup
        # ----------------------------------

        executable = shutil.which(
            application
        )

        if executable:
            return executable

        # ----------------------------------
        # Running process lookup
        # ----------------------------------

        for process in psutil.process_iter(
            ["name", "exe"]
        ):

            try:

                name = (
                    process.info["name"] or ""
                ).lower()

                exe = (
                    process.info["exe"] or ""
                )

                if application.lower() in name:

                    if exe and Path(exe).exists():
                        return exe

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess,
            ):
                continue
            
        registry_path = self._resolve_from_registry(
        application
        )

        if registry_path:
            return registry_path

        raise FileNotFoundError(
            f"Unable to locate '{application}'."
        )
        
        
    
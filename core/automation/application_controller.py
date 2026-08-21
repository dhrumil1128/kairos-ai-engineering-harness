"""
File: core/automation/application_controller.py

Purpose:
Launch and manage desktop applications securely.

Architecture:

Desktop Agent
      ↓
ApplicationController
      ↓
Process Manager
      ↓
Windows Operating System

Future Roadmap
--------------

V1:
- Launch applications
- List running processes
- Security whitelist

V2:
- Terminate applications
- Restart applications
- Focus launched applications

V3:
- Session restoration
- Process monitoring
- Crash recovery

V4:
- Autonomous application orchestration
"""

from __future__ import annotations


import subprocess


import psutil
from core.automation.application_resolver import (
    ApplicationResolver,
)

class ApplicationController:
    """
    Manage desktop applications.
    """
    def __init__(self) -> None:
        """
        Initialize controller.
        """

        self.resolver = (
            ApplicationResolver()
        )
        
        
    _ALLOWED_APPLICATIONS = {
        "code": "Code",
        "notepad": "notepad",
        "calc": "calc",
        "calculator": "calc",
        "explorer": "explorer",
        "cmd": "cmd",
        "powershell": "powershell",
        "wt": "wt",
        "chrome": "chrome",
        "firefox": "firefox",
        "msedge": "msedge",
    }

    _BLOCKED_EXECUTABLES = {
        "malware.exe",
        "virus.exe",
        "ransomware.exe",
    }

    def launch(self, application: str) -> str:
        """
        Launch an approved application.

        Raises:
            PermissionError
            FileNotFoundError
        """

        if not application:
            raise ValueError("Application name cannot be empty.")

        name = application.strip()

        if name.lower() in self._BLOCKED_EXECUTABLES:
            raise PermissionError(
                f"Blocked application: {name}"
            )

        executable = (
            self._ALLOWED_APPLICATIONS.get(
                name.lower(),
                name,
            )
        )

        executable_path = (
            self.resolver.resolve(
                executable
            )
        )

        process = subprocess.Popen(
            [executable_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        return (
            f"Launched: {name} "
            f"(PID={process.pid})"
        )

    def list_processes(self) -> list[dict]:
        """
        Return running processes.
        """

        processes: list[dict] = []

        for proc in psutil.process_iter(
            ["pid", "name"]
        ):
            try:
                info = proc.info

                processes.append(
                    {
                        "pid": info["pid"],
                        "name": info["name"],
                    }
                )

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess,
            ):
                continue

        return processes

    def is_running(
        self,
        application: str,
    ) -> bool:
        """
        Check if an application is running.
        """

        application = application.lower()

        for proc in psutil.process_iter(
            ["name"]
        ):
            try:
                name = (
                    proc.info["name"] or ""
                ).lower()

                if application in name:
                    return True

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess,
            ):
                continue

        return False

    def terminate(
        self,
        pid: int,
    ) -> bool:
        """
        Terminate a process.
        """

        try:
            process = psutil.Process(pid)
            process.terminate()
            process.wait(timeout=5)
            return True

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.TimeoutExpired,
        ):
            return False
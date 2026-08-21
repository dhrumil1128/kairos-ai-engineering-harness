"""
Process launching for the existing KAIROS CLI.
"""

from __future__ import annotations

import logging
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from launcher.utils import RuntimeEnvironment


@dataclass(frozen=True)
class CliLaunchResult:
    """
    Result of launching and waiting for the CLI.
    """

    return_code: int
    command: list[str]


class CliProcessLauncher:
    """
    Launch the existing CLI entrypoint without modifying it.
    """

    def __init__(
        self,
        environment: RuntimeEnvironment,
        logger: logging.Logger,
    ) -> None:
        self.environment = environment
        self.logger = logger

    def launch_and_wait(self) -> CliLaunchResult:
        """
        Start main.py and wait for the CLI process to exit.
        """

        main_path = self.find_main_py()

        if main_path is None:
            raise FileNotFoundError(
                "Unable to locate main.py for the KAIROS CLI."
            )

        command = self.build_command(main_path)

        self.logger.info("Launching CLI: %s", command)

        process = subprocess.Popen(
            command,
            cwd=str(main_path.parent),
        )
        return_code = process.wait()

        self.logger.info("CLI exited with return code %s", return_code)

        return CliLaunchResult(
            return_code=return_code,
            command=command,
        )

    def build_command(
        self,
        main_path: Path,
    ) -> list[str]:
        """
        Build the command used to execute the existing CLI.

        In development, sys.executable is the active Python interpreter.
        In a frozen launcher, sys.executable is the launcher executable
        itself, so use an available Python launcher/interpreter instead.
        """

        if not self.environment.frozen:
            return [
                sys.executable,
                str(main_path),
            ]

        for candidate in (
            "py",
            "python",
            "python3",
        ):
            executable = shutil.which(candidate)

            if executable:
                command = [executable]

                if candidate == "py":
                    command.append("-3")

                command.append(str(main_path))
                return command

        raise FileNotFoundError(
            "Unable to locate a Python interpreter to launch main.py."
        )

    def find_main_py(self) -> Path | None:
        """
        Locate the existing CLI entrypoint.
        """

        candidates = [
            self.environment.project_root / "main.py",
            self.environment.executable_dir / "main.py",
        ]

        if self.environment.bundled_root:
            candidates.append(
                self.environment.bundled_root / "main.py"
            )

        for candidate in candidates:
            if candidate.exists():
                return candidate.resolve()

        return None

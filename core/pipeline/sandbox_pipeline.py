from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path
from typing import Any

from core.logging.kairos_logger import KairosLogger
from core.pipeline.path_resolution import resolve_output_path
from core.pipeline.pipeline_context import PipelineContext
from core.pipeline.pipeline_result import PipelineResult
from core.sandbox.sandbox_config import SandboxConfig
from core.sandbox.execution_command_resolver import ExecutionCommandResolver


class SandboxPipeline:
    """
    Run generated projects in an isolated, read-only sandbox stage.
    """

    def __init__(
        self,
        filesystem,
    ) -> None:
        self.filesystem = filesystem
        self.logger = KairosLogger("sandbox")
        self.command_resolver = ExecutionCommandResolver()

    @property
    def name(self) -> str:
        return "sandbox"

    def supports(
        self,
        pipeline: str,
    ) -> bool:
        return pipeline == self.name

    def execute(
        self,
        context: PipelineContext,
        architecture: dict[str, Any],
        implementation: dict[str, Any],
    ) -> PipelineResult:
        self.logger.info("Sandbox Started")
        self.logger.info("Running Project")

        started = time.perf_counter()
        project_path = Path(context.generated_project)
        command = self.command_resolver.resolve(
            project_path=str(project_path),
            architecture=architecture
        )

        if command is None:
            report = self._report(
                success=False,
                status="failed",
                runtime="unknown",
                command=[],
                stdout="",
                stderr="No supported project entry point found.",
                exit_code=-1,
                started=started,
                exception=None,
            )
            self._write_report(context, report)
            return PipelineResult.failure_result(
                pipeline=self.name,
                data=report,
            )

        try:
            with tempfile.TemporaryDirectory(prefix="kairos_sandbox_") as temp_dir:
                isolated_project = Path(temp_dir) / "project"
                self._copy_project(project_path, isolated_project)
                process = self._run_command(command, isolated_project)
                report = self._report(
                    success=process.returncode == 0,
                    status=(
                        "success"
                        if process.returncode == 0
                        else "failed"
                    ),
                    runtime=command["runtime"],
                    command=command["commands"],
                    stdout=process.stdout,
                    stderr=process.stderr,
                    exit_code=process.returncode,
                    started=started,
                    exception=None,
                )
        except subprocess.TimeoutExpired as error:
            report = self._report(
                success=False,
                status="failed",
                runtime=command["runtime"],
                command=command["commands"],
                stdout=error.stdout or "",
                stderr=error.stderr or "Sandbox execution timed out.",
                exit_code=-2,
                started=started,
                exception="TimeoutExpired",
            )
        except Exception as error:
            report = self._report(
                success=False,
                status="failed",
                runtime=command["runtime"],
                command=command["commands"],
                stdout="",
                stderr=str(error),
                exit_code=-3,
                started=started,
                exception=traceback.format_exc(),
            )

        self._write_report(context, report)

        if report["success"]:
            self.logger.success("Runtime Successful")
            self.logger.success("Sandbox Completed")
            return PipelineResult.success_result(
                pipeline=self.name,
                data=report,
            )

        self.logger.error("Sandbox execution failed")
        self.logger.info("Sandbox Completed")
        return PipelineResult.failure_result(
            pipeline=self.name,
            data=report,
        )

    

    def _run_command(
        self,
        command: dict[str, Any],
        cwd: Path,
    ) -> subprocess.CompletedProcess:
        requirements_file = cwd / "requirements.txt"

        if (
            command["runtime"] == "python"
            and requirements_file.exists()
        ):
            self.logger.info("Installing Python dependencies...")

            python_exe = self.command_resolver._resolve_python_executable()
            install = subprocess.run(
                [
                    python_exe,
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    str(requirements_file),
                ],
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=SandboxConfig.EXECUTION_TIMEOUT,
                shell=False,
            )

            if install.returncode != 0:
                return subprocess.CompletedProcess(
                    args=install.args,
                    returncode=install.returncode,
                    stdout=install.stdout,
                    stderr=install.stderr,
                )

            self.logger.success("Dependencies installed.")
        stdout = []
        stderr = []
        last_process = None

        for step in command["commands"]:
            env = os.environ.copy()
            env["PYTHONPATH"] = str(cwd)
            process = subprocess.Popen(
            step,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False,
            env=env,
        )
            
            try:
                process.wait(timeout=SandboxConfig.EXECUTION_TIMEOUT)

                out, err = process.communicate()

                stdout.append(out or "")
                stderr.append(err or "")

                last_process = subprocess.CompletedProcess(
                    args=step,
                    returncode=process.returncode,
                    stdout=out or "",
                    stderr=err or "",
                )

                if process.returncode != 0:
                    break

            except subprocess.TimeoutExpired:
                try:
                    process.terminate()

                    out, err = process.communicate(timeout=5)

                except Exception:
                    process.kill()

                    out, err = process.communicate()

                stdout.append(out or "")

                timeout_report = (
                    f"Sandbox execution timed out.\n"
                    f"Command: {' '.join(step)}\n"
                    f"Working Directory: {cwd}\n\n"
                    f"STDOUT:\n{out or '<empty>'}\n\n"
                    f"STDERR:\n{err or '<empty>'}"
                )

                stderr.append(timeout_report)

                last_process = subprocess.CompletedProcess(
                    args=step,
                    returncode=-2,
                    stdout=out or "",
                    stderr=timeout_report,
                )

                break

        return subprocess.CompletedProcess(
            args=command["commands"],
            returncode=last_process.returncode if last_process else -1,
            stdout="".join(stdout),
            stderr="".join(stderr),
        )

    def _copy_project(
        self,
        source: Path,
        destination: Path,
    ) -> None:
        ignore = shutil.ignore_patterns(
            ".git",
            "__pycache__",
            ".pytest_cache",
            ".venv",
            "venv",
        )
        shutil.copytree(
            source,
            destination,
            ignore=ignore,
        )

    def _report(
        self,
        *,
        success: bool,
        status: str,
        runtime: str,
        command: list[list[str]],
        stdout: str,
        stderr: str,
        exit_code: int,
        started: float,
        exception: str | None,
    ) -> dict[str, Any]:
        warnings = []
        errors = []

        if stderr:
            errors.append(stderr)

        if "ModuleNotFoundError" in stderr or "ImportError" in stderr:
            errors.append("dependency failure")

        if "SyntaxError" in stderr:
            errors.append("syntax failure")

        if "Traceback" in stderr:
            errors.append("runtime exception")

        if "warning" in stderr.lower():
            warnings.append(stderr)

        if exception:
            errors.append("runtime exception")

        return {
            "success": success,
            "status": status,
            "logs": {
                "stdout": stdout,
                "stderr": stderr,
            },
            "errors": errors,
            "warnings": warnings,
            "runtime": runtime,
            "exit_code": exit_code,
            "execution_time": round(time.perf_counter() - started, 4),
            "command": command,
            "exception": exception,
            "read_only": True,
        }

    def _write_report(
        self,
        context: PipelineContext,
        report: dict[str, Any],
    ) -> None:
        self.filesystem.execute(
            "write",
            resolve_output_path(
                context.generated_project,
                ".kairos",
                "sandbox.json",
            ),
            json.dumps(report, indent=2),
        )

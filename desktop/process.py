"""
Runtime bridge between the desktop presentation layer and the existing CLI.
"""

from __future__ import annotations

import io
import logging
import os
import queue
import sys
import threading
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Callable, Iterator

from PySide6.QtCore import QObject, Signal

from desktop.utils import format_exception


class QueueInput(io.TextIOBase):
    """
    Blocking text input stream backed by terminal host submissions.
    """

    def __init__(self) -> None:
        super().__init__()
        self._queue: queue.Queue[str | None] = queue.Queue()
        self._closed = threading.Event()

    @property
    def encoding(self) -> str:
        return "utf-8"

    def readable(self) -> bool:
        return True

    def isatty(self) -> bool:
        return True

    def readline(self, size: int = -1) -> str:
        if self._closed.is_set():
            return ""

        value = self._queue.get()

        if value is None:
            return ""

        line = value if value.endswith("\n") else f"{value}\n"

        if size is not None and size >= 0:
            return line[:size]

        return line

    def submit(self, text: str) -> None:
        if not self._closed.is_set():
            self._queue.put(text)

    def close_stream(self) -> None:
        self._closed.set()
        self._queue.put(None)


class SignalOutput(io.TextIOBase):
    """
    Text output stream that emits Qt signals.
    """

    def __init__(self, callback: Callable[[str], None]) -> None:
        super().__init__()
        self._callback = callback

    @property
    def encoding(self) -> str:
        return "utf-8"

    def writable(self) -> bool:
        return True

    def isatty(self) -> bool:
        return True

    @property
    def columns(self) -> int:
        value = os.environ.get("COLUMNS", "120")
        return int(value) if value.isdigit() else 120

    def write(self, text: str) -> int:
        if text:
            self._callback(text)

        return len(text)

    def flush(self) -> None:
        return


@dataclass(frozen=True)
class StreamState:
    """
    Original process streams to restore after the CLI exits.
    """

    stdin: io.TextIOBase
    stdout: io.TextIOBase
    stderr: io.TextIOBase


class KairosRuntime(QObject):
    """
    Host the existing KAIROS CLI inside the desktop application.
    """

    started = Signal()
    output_received = Signal(str)
    error_received = Signal(str)
    finished = Signal(int)

    def __init__(self, logger: logging.Logger) -> None:
        super().__init__()
        self._logger = logger
        self._input = QueueInput()
        self._thread: threading.Thread | None = None
        self._exit_code = 0
        self._lock = threading.Lock()

    def start(self) -> None:
        """
        Start the existing CLI on a background runtime thread.
        """

        with self._lock:
            if self._thread and self._thread.is_alive():
                return

            self._thread = threading.Thread(
                target=self._run,
                name="KairosRuntime",
                daemon=True,
            )
            self._thread.start()

    def submit_input(self, text: str) -> None:
        """
        Send a submitted terminal line to the CLI.
        """

        self._input.submit(text)

    def stop(self) -> None:
        """
        Ask the CLI to exit and unblock pending reads.
        """

        self._input.submit("exit")
        self._input.close_stream()

    def is_running(self) -> bool:
        return bool(self._thread and self._thread.is_alive())

    def _run(self) -> None:
        self.started.emit()
        self._logger.info("KAIROS runtime started.")

        try:
            with self._redirected_streams():
                from main import main as cli_main

                result = cli_main()
                self._exit_code = int(result or 0)
        except SystemExit as error:
            self._exit_code = int(error.code or 0) if isinstance(error.code, int) else 1
        except BaseException as error:
            self._exit_code = 1
            self._logger.exception("KAIROS runtime crashed.")
            self.error_received.emit(f"\n[KAIROS Runtime Error] {format_exception(error)}\n")
        finally:
            self._input.close_stream()
            self._logger.info("KAIROS runtime finished with code %s.", self._exit_code)
            self.finished.emit(self._exit_code)

    @contextmanager
    def _redirected_streams(self) -> Iterator[None]:
        original = StreamState(
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        output = SignalOutput(self.output_received.emit)
        error = SignalOutput(self.error_received.emit)

        sys.stdin = self._input
        sys.stdout = output
        sys.stderr = error

        try:
            yield
        finally:
            sys.stdin = original.stdin
            sys.stdout = original.stdout
            sys.stderr = original.stderr

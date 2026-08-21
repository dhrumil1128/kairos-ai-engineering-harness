"""
Embedded terminal host for the KAIROS desktop application.
"""

from __future__ import annotations

import os
import re

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QKeyEvent, QTextCharFormat, QTextCursor, QResizeEvent
from PySide6.QtWidgets import QApplication, QPlainTextEdit, QVBoxLayout, QWidget

from desktop.process import KairosRuntime
from desktop.theme import DesktopTheme


class TerminalView(QPlainTextEdit):
    """
    Terminal-like text surface that keeps history read-only.
    """

    line_submitted = Signal(str)

    def __init__(self, theme: DesktopTheme) -> None:
        super().__init__()
        self.setObjectName("TerminalView")
        self.setFont(theme.mono_font())
        self.setUndoRedoEnabled(False)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setTabStopDistance(36)
        self.setCursorWidth(8)
        self._input_start = 0
        self._theme = theme
        self._ansi = AnsiFormatter(theme)
        self._sync_terminal_size()

    def append_output(self, text: str) -> None:
        """
        Append runtime output and move the editable boundary.
        """

        self.moveCursor(QTextCursor.MoveOperation.End)
        self._sync_terminal_size()
        self._insert_terminal_text(text)
        self._input_start = self.document().characterCount() - 1
        self.moveCursor(QTextCursor.MoveOperation.End)
        self.ensureCursorVisible()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self._sync_terminal_size()
        super().resizeEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()
        modifiers = event.modifiers()

        if modifiers == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_L:
            self.clear()
            self._input_start = 0
            return

        if modifiers == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_C:
            self.insertPlainText("^C\n")
            self._input_start = self.document().characterCount() - 1
            return

        if key in (Qt.Key.Key_Left, Qt.Key.Key_Up, Qt.Key.Key_PageUp):
            if self.textCursor().position() <= self._input_start:
                return

        if key == Qt.Key.Key_Home:
            cursor = self.textCursor()
            cursor.setPosition(self._input_start)
            self.setTextCursor(cursor)
            return

        if key in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete):
            if self.textCursor().position() <= self._input_start:
                return

        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            line = self._current_input()
            self.moveCursor(QTextCursor.MoveOperation.End)
            self.insertPlainText("\n")
            self._input_start = self.document().characterCount() - 1
            self.line_submitted.emit(line)
            return

        if modifiers == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_V:
            self._paste_text()
            return

        if self.textCursor().position() < self._input_start:
            self.moveCursor(QTextCursor.MoveOperation.End)

        super().keyPressEvent(event)

    def insertFromMimeData(self, source) -> None:  # type: ignore[no-untyped-def]
        self._paste_text(source.text())

    def _paste_text(self, text: str | None = None) -> None:
        clipboard_text = text if text is not None else self.clipboard_text()

        if not clipboard_text:
            return

        self.moveCursor(QTextCursor.MoveOperation.End)
        self.insertPlainText(clipboard_text.replace("\r\n", "\n"))

    def clipboard_text(self) -> str:
        return QApplication.clipboard().text()

    def _current_input(self) -> str:
        text = self.toPlainText()
        return text[self._input_start :]

    def _insert_terminal_text(self, text: str) -> None:
        cursor = self.textCursor()

        for chunk, char_format in self._ansi.parse(text):
            if chunk == "\r":
                cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
                continue

            if chunk:
                cursor.insertText(chunk, char_format)

        self.setTextCursor(cursor)

    def _sync_terminal_size(self) -> None:
        metrics = self.fontMetrics()
        char_width = max(1, metrics.horizontalAdvance("M"))
        columns = max(40, int(self.viewport().width() / char_width) - 2)
        rows = max(10, int(self.viewport().height() / max(1, metrics.lineSpacing())))
        os.environ["COLUMNS"] = str(columns)
        os.environ["LINES"] = str(rows)


class AnsiFormatter:
    """
    Translate terminal SGR sequences into QTextCharFormat spans.
    """

    CSI_PATTERN = re.compile(r"\x1b\[([?0-9;:]*)?([@-~])")
    ANSI_16 = {
        30: "#000000",
        31: "#CD3131",
        32: "#0DBC79",
        33: "#E5E510",
        34: "#2472C8",
        35: "#BC3FBC",
        36: "#11A8CD",
        37: "#E5E5E5",
        90: "#666666",
        91: "#F14C4C",
        92: "#23D18B",
        93: "#F5F543",
        94: "#3B8EEA",
        95: "#D670D6",
        96: "#29B8DB",
        97: "#FFFFFF",
    }

    ANSI_16_BG = {code + 10: color for code, color in ANSI_16.items() if code < 40}
    ANSI_16_BG.update({code + 10: color for code, color in ANSI_16.items() if code >= 90})

    def __init__(self, theme: DesktopTheme) -> None:
        self._theme = theme
        self._format = QTextCharFormat()
        self._format.setForeground(QColor(theme.terminal_text))

    def parse(self, text: str) -> list[tuple[str, QTextCharFormat]]:
        repaired = self._repair_mojibake(text)
        spans: list[tuple[str, QTextCharFormat]] = []
        position = 0

        for match in self.CSI_PATTERN.finditer(repaired):
            if match.start() > position:
                spans.append((repaired[position : match.start()], QTextCharFormat(self._format)))

            if match.group(2) == "m":
                self._apply_sgr(match.group(1) or "0")

            position = match.end()

        if position < len(repaired):
            spans.append((repaired[position:], QTextCharFormat(self._format)))

        return spans

    def _apply_sgr(self, sequence: str) -> None:
        parts = self._parts(sequence)
        index = 0

        while index < len(parts):
            code = parts[index]

            if code == 0:
                self._reset()
            elif code == 1:
                self._format.setFontWeight(700)
            elif code == 3:
                self._format.setFontItalic(True)
            elif code == 4:
                self._format.setFontUnderline(True)
            elif code == 22:
                self._format.setFontWeight(400)
            elif code == 23:
                self._format.setFontItalic(False)
            elif code == 24:
                self._format.setFontUnderline(False)
            elif code == 39:
                self._format.setForeground(QColor(self._theme.terminal_text))
            elif code == 49:
                self._format.clearBackground()
            elif code in self.ANSI_16:
                self._format.setForeground(QColor(self.ANSI_16[code]))
            elif code in self.ANSI_16_BG:
                self._format.setBackground(QColor(self.ANSI_16_BG[code]))
            elif code in (38, 48):
                index = self._apply_extended_color(parts, index)

            index += 1

    def _apply_extended_color(self, parts: list[int], index: int) -> int:
        target = parts[index]

        if index + 1 >= len(parts):
            return index

        mode = parts[index + 1]

        if mode == 2 and index + 4 < len(parts):
            color = QColor(parts[index + 2], parts[index + 3], parts[index + 4])
            self._set_color(target, color)
            return index + 4

        if mode == 5 and index + 2 < len(parts):
            color = QColor(self._color_256(parts[index + 2]))
            self._set_color(target, color)
            return index + 2

        return index + 1

    def _set_color(self, target: int, color: QColor) -> None:
        if target == 38:
            self._format.setForeground(color)
        else:
            self._format.setBackground(color)

    def _reset(self) -> None:
        self._format = QTextCharFormat()
        self._format.setForeground(QColor(self._theme.terminal_text))

    def _parts(self, sequence: str) -> list[int]:
        values = sequence.replace(":", ";").split(";")
        return [int(value) if value else 0 for value in values]

    def _color_256(self, code: int) -> str:
        if code < 16:
            return self.ANSI_16.get(30 + (code % 8), self._theme.terminal_text)

        if 16 <= code <= 231:
            value = code - 16
            red = value // 36
            green = (value % 36) // 6
            blue = value % 6
            channels = [0 if channel == 0 else 55 + channel * 40 for channel in (red, green, blue)]
            return "#{:02X}{:02X}{:02X}".format(*channels)

        gray = 8 + (code - 232) * 10
        return "#{0:02X}{0:02X}{0:02X}".format(gray)

    def _repair_mojibake(self, text: str) -> str:
        if not any(marker in text for marker in ("\u00c3", "\u00c2", "\u00e2")):
            return text

        try:
            repaired = self._mojibake_bytes(text).decode("utf-8")
        except UnicodeError:
            return text

        return repaired if repaired.count("\ufffd") <= text.count("\ufffd") else text

    def _mojibake_bytes(self, text: str) -> bytes:
        values = bytearray()

        for character in text:
            try:
                encoded = character.encode("cp1252")
            except UnicodeEncodeError:
                ordinal = ord(character)

                if ordinal <= 0xFF:
                    values.append(ordinal)
                    continue

                values.extend(character.encode("utf-8"))
                continue

            values.extend(encoded)

        return bytes(values)


class TerminalHost(QWidget):
    """
    Presentation-layer host for an embedded KAIROS terminal session.
    """

    def __init__(
        self,
        runtime: KairosRuntime,
        theme: DesktopTheme,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._runtime = runtime
        self._theme = theme
        self._view = TerminalView(theme)
        self._build_layout()
        self._connect_runtime()

    def start(self) -> None:
        self._runtime.start()

    def stop(self) -> None:
        self._runtime.stop()

    def write_system_line(self, text: str) -> None:
        self._view.append_output(f"{text}\n")

    def _build_layout(self) -> None:
        self.setObjectName("TerminalPanel")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._view)

    def _connect_runtime(self) -> None:
        self._runtime.started.connect(
            lambda: self.write_system_line("[KAIROS Desktop] Runtime attached.")
        )
        self._runtime.output_received.connect(self._view.append_output)
        self._runtime.error_received.connect(self._view.append_output)
        self._runtime.finished.connect(self._on_finished)
        self._view.line_submitted.connect(self._runtime.submit_input)

    def _on_finished(self, exit_code: int) -> None:
        self.write_system_line(f"[KAIROS Desktop] Runtime exited with code {exit_code}.")

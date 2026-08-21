"""
Main KAIROS desktop window.
"""

from __future__ import annotations

import ctypes
import ctypes.wintypes
import logging
from pathlib import Path

from PySide6.QtCore import QEvent, QPoint, Qt
from PySide6.QtGui import QCloseEvent, QCursor, QIcon, QMouseEvent, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from desktop.process import KairosRuntime
from desktop.terminal import TerminalHost
from desktop.theme import DesktopTheme
from desktop.utils import DesktopConfig


class WindowControlButton(QPushButton):
    """
    Title-bar button that invokes its window action directly on mouse release.
    """

    def __init__(
        self,
        text: str,
        action,  # type: ignore[no-untyped-def]
        parent: QWidget,
        object_name: str,
    ) -> None:
        super().__init__(text, parent)
        self._action = action
        self.setObjectName(object_name)
        self.setFixedSize(46, 46)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            event.accept()
            return

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if (
            event.button() == Qt.MouseButton.LeftButton
            and self.rect().contains(event.position().toPoint())
        ):
            self._action()
            event.accept()
            return

        super().mouseReleaseEvent(event)


class WindowTitleBar(QFrame):
    """
    Frameless window header with native-feeling controls.
    """

    def __init__(
        self,
        *,
        window: "MainWindow",
        logo_path: Path | None,
    ) -> None:
        super().__init__(window)
        self._window = window
        self._logo_path = logo_path
        self._maximize_button: QPushButton | None = None
        self._window_buttons: list[QPushButton] = []
        self._runtime_status = QLabel("Runtime: starting")
        self._build()

    @property
    def runtime_status(self) -> QLabel:
        return self._runtime_status

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton and self.is_drag_region(QCursor.pos()):
            self._window.toggle_maximized()
            event.accept()
            return

        super().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton and self.is_drag_region(QCursor.pos()):
            handle = self._window.windowHandle()

            if handle:
                handle.startSystemMove()
                event.accept()
                return

        super().mousePressEvent(event)

    def is_drag_region(self, global_position: QPoint) -> bool:
        local_position = self.mapFromGlobal(global_position)

        if not self.rect().contains(local_position):
            return False

        return not isinstance(self.childAt(local_position), QPushButton)

    def is_control_region(self, global_position: QPoint) -> bool:
        for button in self._window_buttons:
            local_position = button.mapFromGlobal(global_position)

            if button.rect().contains(local_position):
                return True

        return False

    def sync_maximize_state(self) -> None:
        if not self._maximize_button:
            return

        self._maximize_button.setText(
            "\ue922" if not self._window.isMaximized() else "\ue923"
        )

    def _build(self) -> None:
        self.setObjectName("TitleBar")
        self.setFixedHeight(46)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(8)

        logo = QLabel()
        logo.setObjectName("TitleLogo")
        logo.setFixedSize(26, 26)
        logo.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        if self._logo_path:
            logo.setPixmap(
                QPixmap(str(self._logo_path)).scaled(
                    26,
                    26,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        else:
            logo.setText("K")
            logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("KAIROS")
        title.setObjectName("TitleText")
        title.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        title.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        self._runtime_status.setObjectName("RuntimeStatus")
        self._runtime_status.setSizePolicy(
            QSizePolicy.Policy.Maximum,
            QSizePolicy.Policy.Preferred,
        )
        self._runtime_status.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            True,
        )

        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(self._runtime_status)
        layout.addStretch(1)
        layout.addWidget(self._window_button("\ue921", self._window.minimize_window))

        self._maximize_button = self._window_button(
            "\ue922",
            self._window.toggle_maximized,
        )
        layout.addWidget(self._maximize_button)
        layout.addWidget(self._window_button("\ue8bb", self._window.close, "CloseButton"))

    def _window_button(
        self,
        text: str,
        slot,  # type: ignore[no-untyped-def]
        object_name: str = "WindowButton",
    ) -> QPushButton:
        button = WindowControlButton(text, slot, self, object_name)
        self._window_buttons.append(button)
        return button


class MainWindow(QMainWindow):
    """
    Professional desktop shell for current and future KAIROS modules.
    """

    def __init__(
        self,
        *,
        config: DesktopConfig,
        theme: DesktopTheme,
        runtime: KairosRuntime,
        logger: logging.Logger,
        icon_path: Path | None = None,
        logo_path: Path | None = None,
    ) -> None:
        super().__init__()
        self._config = config
        self._theme = theme
        self._runtime = runtime
        self._logger = logger
        self._icon_path = icon_path
        self._logo_path = logo_path
        self._terminal = TerminalHost(runtime, theme, self)
        self._title_bar: WindowTitleBar | None = None
        self._build_window()

    def start_runtime(self) -> None:
        self._terminal.start()

    def minimize_window(self) -> None:
        self.showMinimized()

    def toggle_maximized(self) -> None:
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

        self._sync_title_bar()

    def closeEvent(self, event: QCloseEvent) -> None:
        self._logger.info("Desktop window closing.")
        self._terminal.stop()
        super().closeEvent(event)

    def changeEvent(self, event) -> None:  # type: ignore[no-untyped-def]
        super().changeEvent(event)

        if event.type() == QEvent.Type.WindowStateChange:
            self._sync_title_bar()

    def nativeEvent(self, event_type, message):  # type: ignore[no-untyped-def]
        if event_type not in ("windows_generic_MSG", "windows_dispatcher_MSG"):
            return False, 0

        msg = ctypes.wintypes.MSG.from_address(int(message))

        if msg.message != 0x0084:
            return False, 0

        border = 7
        cursor_position = QCursor.pos()
        x = cursor_position.x()
        y = cursor_position.y()
        top_left = self.mapToGlobal(QPoint(0, 0))
        width = self.width()
        height = self.height()
        local_x = x - top_left.x()
        local_y = y - top_left.y()

        if self._title_bar and self._title_bar.is_control_region(QPoint(x, y)):
            HTCLIENT = 1

        if self._title_bar and self._title_bar.is_control_region(QPoint(x, y)):
            return True, HTCLIENT

        if not self.isMaximized():
            left = local_x <= border
            right = local_x >= width - border
            top = local_y <= border
            bottom = local_y >= height - border

            if top and left:
                return True, 13
            if top and right:
                return True, 14
            if bottom and left:
                return True, 16
            if bottom and right:
                return True, 17
            if left:
                return True, 10
            if right:
                return True, 11
            if top:
                return True, 12
            if bottom:
                return True, 15

        return False, 0

    def _build_window(self) -> None:
        self.setWindowTitle(self._config.window_title)
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowMinimizeButtonHint
            | Qt.WindowType.WindowMaximizeButtonHint
        )
        self.resize(*self._config.initial_window_size)
        self.setMinimumSize(*self._config.minimum_window_size)

        if self._icon_path:
            self.setWindowIcon(QIcon(str(self._icon_path)))

        shell = QFrame()
        shell.setObjectName("AppShell")
        root = QVBoxLayout(shell)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self._title_bar = WindowTitleBar(
            window=self,
            logo_path=self._logo_path,
        )

        root.addWidget(self._title_bar)
        root.addWidget(self._workspace(), 1)

        self.setCentralWidget(shell)
        self._runtime.started.connect(
            lambda: self._set_runtime_status("Runtime: active")
        )
        self._runtime.finished.connect(
            lambda code: self._set_runtime_status(f"Runtime: exited {code}")
        )

    def _workspace(self) -> QWidget:
        workspace = QWidget()
        workspace.setObjectName("Workspace")
        workspace.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout = QVBoxLayout(workspace)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self._terminal.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        layout.addWidget(self._terminal, 1)

        return workspace

    def _set_runtime_status(self, value: str) -> None:
        if self._title_bar:
            self._title_bar.runtime_status.setText(value)

    def _sync_title_bar(self) -> None:
        if self._title_bar:
            self._title_bar.sync_maximize_state()

    def _signed_low_word(self, value: int) -> int:
        word = value & 0xFFFF
        return word - 0x10000 if word & 0x8000 else word

    def _signed_high_word(self, value: int) -> int:
        word = (value >> 16) & 0xFFFF
        return word - 0x10000 if word & 0x8000 else word

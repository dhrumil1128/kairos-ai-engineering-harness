"""
PySide6 splash screen for KAIROS desktop.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QGraphicsOpacityEffect,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)

from desktop.theme import DesktopTheme
from desktop.utils import DesktopConfig


class SplashScreen(QWidget):
    """
    Display the startup splash with fade and loading animation.
    """

    def __init__(
        self,
        config: DesktopConfig,
        theme: DesktopTheme,
        splash_path: Path | None,
    ) -> None:
        super().__init__()
        self._config = config
        self._theme = theme
        self._splash_path = splash_path
        self._progress = QProgressBar()
        self._opacity = QGraphicsOpacityEffect(self)
        self._timer = QTimer(self)
        self._build_ui()

    def show_and_close(self, on_finished: Callable[[], None]) -> None:
        """
        Show splash, fade in, then fade out and call the continuation.
        """

        self.setGraphicsEffect(self._opacity)
        self._opacity.setOpacity(0.0)
        self.show()

        fade_in = self._animation(0.0, 1.0)
        fade_in.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

        self._timer.timeout.connect(self._advance_progress)
        self._timer.start(42)

        QTimer.singleShot(
            self._config.splash_timeout_ms,
            lambda: self._close_with_fade(on_finished),
        )

    def _build_ui(self) -> None:
        self.setWindowTitle(self._config.window_title)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.SplashScreen
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setFixedSize(760, 440)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(56, 44, 56, 30)
        layout.setSpacing(18)

        image = QLabel()
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if self._splash_path:
            pixmap = QPixmap(str(self._splash_path))
            image.setPixmap(
                pixmap.scaled(
                    420,
                    260,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        else:
            image.setText("KAIROS")
            image.setStyleSheet("font-size: 48px; font-weight: 700;")

        title = QLabel("Starting KAIROS")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: 600;")

        subtitle = QLabel("Preparing the command intelligence workspace")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"color: {self._theme.muted};")

        self._progress.setRange(0, 100)
        self._progress.setValue(0)
        self._progress.setTextVisible(False)
        self._progress.setFixedHeight(4)
        self._progress.setStyleSheet(
            f"""
            QProgressBar {{
                background: {self._theme.surface_raised};
                border: none;
                border-radius: 2px;
            }}
            QProgressBar::chunk {{
                background: {self._theme.red};
                border-radius: 2px;
            }}
            """
        )

        layout.addStretch(1)
        layout.addWidget(image)
        layout.addStretch(1)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)
        layout.addWidget(self._progress)

        self.setStyleSheet(
            f"""
            SplashScreen {{
                background: {self._theme.background};
            }}
            """
        )

    def _advance_progress(self) -> None:
        value = self._progress.value()
        self._progress.setValue((value + 3) % 101)

    def _close_with_fade(self, on_finished: Callable[[], None]) -> None:
        self._timer.stop()
        fade_out = self._animation(1.0, 0.0)
        fade_out.finished.connect(self.close)
        fade_out.finished.connect(on_finished)
        fade_out.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

    def _animation(self, start: float, end: float) -> QPropertyAnimation:
        animation = QPropertyAnimation(self._opacity, b"opacity", self)
        animation.setDuration(self._config.splash_fade_ms)
        animation.setStartValue(start)
        animation.setEndValue(end)
        animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        return animation

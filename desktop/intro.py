"""
Intro video playback for the KAIROS desktop application.
"""

from __future__ import annotations

import logging
from pathlib import Path

from PySide6.QtCore import QTimer, QUrl, Signal
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QVBoxLayout, QWidget
#from PySide6.QtMultimedia import QAudioOutput
from desktop.theme import DesktopTheme
from desktop.utils import DesktopConfig


class IntroPlayer(QWidget):
    """
    Auto-play intro.mp4 with no visible playback controls.
    """

    finished = Signal()

    def __init__(
        self,
        config: DesktopConfig,
        theme: DesktopTheme,
        intro_path: Path | None,
        logger: logging.Logger,
    ) -> None:
        super().__init__()
        self._config = config
        self._theme = theme
        self._intro_path = intro_path
        self._logger = logger
        self._player = QMediaPlayer(self)
        #self._audio = QAudioOutput(self)
        #self._audio.setVolume(1.0)
        #self._audio.setMuted(False)
        #self._player.setAudioOutput(self._audio)
        self._video = QVideoWidget(self)
        self._build_ui()
        self._connect_player()

    def play_or_skip(self) -> None:
        """
        Play the intro if available, otherwise continue immediately.
        """

        if self._intro_path is None:
            self._logger.info("intro.mp4 not found; skipping intro.")
            self.finished.emit()
            return

        self.showFullScreen()
        self._player.setVideoOutput(self._video)
        self._player.setSource(QUrl.fromLocalFile(str(self._intro_path)))
        self._player.play()

        QTimer.singleShot(self._config.intro_timeout_ms, self._finish)

    def keyPressEvent(self, event) -> None:  # type: ignore[no-untyped-def]
        self._finish()

    def _build_ui(self) -> None:
        self.setWindowTitle(self._config.window_title)
        self.setStyleSheet(f"background: {self._theme.background};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._video)

    def _connect_player(self) -> None:
        self._player.mediaStatusChanged.connect(self._on_status_changed)
        self._player.errorOccurred.connect(self._on_error)

    def _on_status_changed(self, status: QMediaPlayer.MediaStatus) -> None:
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self._finish()

    def _on_error(self, error):
        print("=" * 60)
        print("Qt Media Error:", error)
        print("Error String:", self._player.errorString())
        print("=" * 60)

        self._logger.warning(
            "Intro playback failed: %s",
            self._player.errorString(),
        )

        self._finish()

    def _finish(self) -> None:
        if self.isHidden():
            return

        self._player.stop()
        self.close()
        self.finished.emit()

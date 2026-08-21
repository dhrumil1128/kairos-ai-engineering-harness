"""
PySide6 entry point for the KAIROS desktop application.
"""

from __future__ import annotations

import ctypes
import logging
import sys

from pathlib import Path


from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication, QMessageBox

from desktop.assets import AssetResolver
from desktop.intro import IntroPlayer
from desktop.main_window import MainWindow
from desktop.process import KairosRuntime
from desktop.splash import SplashScreen
from desktop.theme import DesktopTheme
from desktop.utils import DesktopConfig, configure_logging, get_runtime_environment


class DesktopApplication:
    """
    Coordinate KAIROS desktop startup and runtime ownership.
    """

    def __init__(self) -> None:
        self.config = DesktopConfig()
        self.environment = get_runtime_environment()
        self.logger = configure_logging(self.config)
        self.assets = AssetResolver(self.environment)
        self.theme = DesktopTheme()
        self.app = self._create_qapplication()
        self.window: MainWindow | None = None
        self.runtime: KairosRuntime | None = None
        self.splash: SplashScreen | None = None
        self.intro: IntroPlayer | None = None

    def run(self) -> int:
        """
        Run the splash, intro, main window, and embedded terminal.
        """

        self.logger.info("KAIROS desktop starting.")
        self._apply_window_icon()

        self.splash = SplashScreen(
            self.config,
            self.theme,
            self.assets.path("splash.png"),
        )
        self.splash.show_and_close(self._play_intro)

        return self.app.exec()

    def _create_qapplication(self) -> QApplication:
        self._enable_high_dpi()

        app = QApplication(sys.argv)
        app.setApplicationName(self.config.app_name)
        app.setOrganizationName(self.config.organization_name)
        app.setQuitOnLastWindowClosed(True)
        self.theme.apply(app)
        return app

    def _play_intro(self) -> None:
        self.intro = IntroPlayer(
            self.config,
            self.theme,
            self.assets.path("intro.mp4"),
            self.logger,
        )
        self.intro.finished.connect(self._show_main_window)
        self.intro.play_or_skip()

    def _show_main_window(self) -> None:
        self.runtime = KairosRuntime(self.logger)
        self.window = MainWindow(
            config=self.config,
            theme=self.theme,
            runtime=self.runtime,
            logger=self.logger,
            icon_path=self.assets.path("kairos.ico"),
            logo_path=self.assets.path("kairos_logo.png"),
        )
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()
        self.window.start_runtime()


    def _apply_window_icon(self) -> None:
        icon_path = self.assets.path("kairos.ico")

        if icon_path:
            from PySide6.QtGui import QIcon

            self.app.setWindowIcon(QIcon(str(icon_path)))

    def _enable_high_dpi(self) -> None:
        if sys.platform != "win32":
            return

        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                return


def show_startup_error(error: BaseException, logger: logging.Logger | None = None) -> None:
    """
    Display startup failures without exposing a console dependency.
    """

    if logger:
        logger.exception("Desktop startup failed.")

    app = QApplication.instance() or QApplication(sys.argv)
    QMessageBox.critical(
        None,
        "KAIROS Startup Error",
        f"KAIROS Desktop could not start.\n\n{type(error).__name__}: {error}",
    )
    app.quit()


def main() -> int:
    """
    Desktop script entry point.
    """

    desktop: DesktopApplication | None = None
    if getattr(sys, "frozen", False):
        env_path = Path(sys.executable).parent / ".env"
    else:
        env_path = Path(__file__).resolve().parent.parent / ".env"

    load_dotenv(env_path)

    try:
        desktop = DesktopApplication()
        return desktop.run()
    except BaseException as error:
        show_startup_error(error, desktop.logger if desktop else None)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

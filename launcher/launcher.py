"""
Main desktop startup coordinator for KAIROS.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from launcher.assets import AssetLocator
from launcher.intro import IntroPlayer
from launcher.process import CliProcessLauncher
from launcher.splash import SplashScreen
from launcher.utils import (
    LauncherConfig,
    RuntimeEnvironment,
    configure_logging,
    get_runtime_environment,
    show_error_dialog,
)
from launcher.window import WindowFactory


@dataclass
class Launcher:
    """
    Coordinate the KAIROS desktop startup experience.
    """

    config: LauncherConfig
    environment: RuntimeEnvironment
    logger: logging.Logger
    assets: AssetLocator
    window_factory: WindowFactory
    process_launcher: CliProcessLauncher

    @classmethod
    def create(cls) -> "Launcher":
        """
        Build the launcher with production defaults.
        """

        config = LauncherConfig()
        environment = get_runtime_environment()
        logger = configure_logging(config)
        assets = AssetLocator(environment)
        window_factory = WindowFactory(config)
        process_launcher = CliProcessLauncher(
            environment=environment,
            logger=logger,
        )

        return cls(
            config=config,
            environment=environment,
            logger=logger,
            assets=assets,
            window_factory=window_factory,
            process_launcher=process_launcher,
        )

    def run(self) -> int:
        """
        Run the startup flow and return the CLI exit code.
        """

        self.logger.info("KAIROS launcher started.")

        self._show_splash()
        self._play_intro()
        self._initialize_environment()

        try:
            result = self.process_launcher.launch_and_wait()
        except Exception as error:
            self.logger.exception("Unable to launch KAIROS CLI.")
            show_error_dialog(
                "KAIROS Startup Error",
                (
                    "KAIROS could not start the command line application.\n\n"
                    f"{error}"
                ),
            )
            return 1

        self.logger.info("KAIROS launcher finished.")

        return result.return_code

    def _show_splash(self) -> None:
        splash = SplashScreen(
            window_factory=self.window_factory,
            config=self.config,
            logger=self.logger,
            splash_path=self.assets.get_asset_path("splash.png"),
            icon_path=self.assets.get_asset_path("kairos.ico"),
        )
        splash.show()

    def _play_intro(self) -> None:
        intro = IntroPlayer(
            window_factory=self.window_factory,
            config=self.config,
            logger=self.logger,
            intro_path=self.assets.get_asset_path("intro.mp4"),
            icon_path=self.assets.get_asset_path("kairos.ico"),
        )
        intro.play()

    def _initialize_environment(self) -> None:
        """
        Reserved for launcher-only startup preparation.
        """

        self.logger.info(
            "Runtime mode: %s",
            "PyInstaller" if self.environment.frozen else "development",
        )


def main() -> int:
    """
    Console/script entrypoint.
    """

    launcher = Launcher.create()
    return launcher.run()


if __name__ == "__main__":
    raise SystemExit(main())

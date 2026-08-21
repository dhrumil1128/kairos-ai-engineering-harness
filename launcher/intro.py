"""
Intro video playback for the KAIROS launcher.
"""

from __future__ import annotations

import logging
import time
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from launcher.utils import LauncherConfig
from launcher.window import WindowFactory


@dataclass
class IntroPlayer:
    """
    Play the optional startup intro video.
    """

    window_factory: WindowFactory
    config: LauncherConfig
    logger: logging.Logger
    intro_path: Path | None = None
    icon_path: Path | None = None

    def play(self) -> None:
        """
        Play intro.mp4 fullscreen when optional video dependencies exist.
        Missing or unplayable video is non-fatal.
        """

        if self.intro_path is None:
            self.logger.info("intro.mp4 not found; skipping intro video.")
            return

        try:
            cv2, image_module, image_tk_module = self._load_video_dependencies()
        except Exception as error:
            self.logger.info("Intro video skipped; video backend unavailable: %s", error)
            return

        capture = cv2.VideoCapture(str(self.intro_path))

        if not capture.isOpened():
            self.logger.warning("Intro video could not be opened: %s", self.intro_path)
            return

        try:
            self._play_capture(
                capture=capture,
                cv2=cv2,
                image_module=image_module,
                image_tk_module=image_tk_module,
            )
        except Exception as error:
            self.logger.warning("Intro video skipped: %s", error)
        finally:
            capture.release()

    def _load_video_dependencies(self) -> tuple[Any, Any, Any]:
        import cv2
        from PIL import Image, ImageTk

        return cv2, Image, ImageTk

    def _play_capture(
        self,
        *,
        capture: Any,
        cv2: Any,
        image_module: Any,
        image_tk_module: Any,
    ) -> None:
        root = self.window_factory.create_window(
            title=self.config.window_title,
            fullscreen=True,
            icon_path=self.icon_path,
        )
        root.configure(background=self.window_factory.theme.background)

        label = tk.Label(
            root,
            background=self.window_factory.theme.background,
            borderwidth=0,
        )
        label.pack(fill="both", expand=True)

        fps = capture.get(cv2.CAP_PROP_FPS) or 30
        delay_ms = max(1, int(1000 / fps))
        started_at = time.monotonic()

        def render_next_frame() -> None:
            if (time.monotonic() - started_at) * 1000 > self.config.intro_timeout_ms:
                root.destroy()
                return

            ok, frame = capture.read()

            if not ok:
                root.destroy()
                return

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = image_module.fromarray(frame)

            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            resampling = getattr(
                getattr(image_module, "Resampling", image_module),
                "LANCZOS",
            )
            image.thumbnail(
                (screen_width, screen_height),
                resampling,
            )

            photo = image_tk_module.PhotoImage(image=image)
            label.configure(image=photo)
            label.image = photo

            root.after(delay_ms, render_next_frame)

        root.bind("<Escape>", lambda _event: root.destroy())
        render_next_frame()
        root.mainloop()

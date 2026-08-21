"""
Splash screen for the KAIROS launcher.
"""

from __future__ import annotations

import logging
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path

from launcher.utils import LauncherConfig
from launcher.window import Theme, WindowFactory


@dataclass
class SplashScreen:
    """
    Display the premium startup splash experience.
    """

    window_factory: WindowFactory
    config: LauncherConfig
    logger: logging.Logger
    splash_path: Path | None = None
    icon_path: Path | None = None
    theme: Theme | None = None

    def show(self) -> None:
        """
        Show the splash screen. Missing assets are non-fatal.
        """

        if self.splash_path is None:
            self.logger.info("splash.png not found; skipping splash screen.")
            return

        theme = self.theme or self.window_factory.theme

        try:
            root = self.window_factory.create_window(
                title=self.config.window_title,
                size=self.config.splash_size,
                icon_path=self.icon_path,
            )
            root.attributes("-alpha", 0.0)

            canvas = tk.Canvas(
                root,
                background=theme.background,
                highlightthickness=0,
            )
            canvas.pack(fill="both", expand=True)

            image = tk.PhotoImage(file=str(self.splash_path))
            self._draw(
                canvas=canvas,
                root=root,
                image=image,
                theme=theme,
            )

            state = {
                "step": 0,
                "loading": 0,
                "closing": 0,
            }

            self._fade_in(root, state)
            self._animate_loading(canvas, root, state, theme)
            root.after(
                self.config.splash_timeout_ms,
                lambda: self._fade_out(root, state),
            )

            root.mainloop()
        except Exception as error:
            self.logger.warning("Splash screen skipped: %s", error)

    def _draw(
        self,
        *,
        canvas: tk.Canvas,
        root: tk.Tk,
        image: tk.PhotoImage,
        theme: Theme,
    ) -> None:
        width, height = self.config.splash_size

        canvas.create_rectangle(
            0,
            0,
            width,
            height,
            fill=theme.background,
            outline=theme.background,
        )
        canvas.create_image(
            width // 2,
            height // 2 - 34,
            image=image,
            anchor="center",
        )
        canvas.image = image
        canvas.create_text(
            width // 2,
            height - 78,
            text="Starting KAIROS",
            fill=theme.text,
            font=("Segoe UI Semibold", 13),
        )
        canvas.create_text(
            width // 2,
            height - 50,
            text="Preparing the command intelligence workspace",
            fill=theme.muted,
            font=("Segoe UI", 10),
        )
        root.update_idletasks()

    def _fade_in(
        self,
        root: tk.Tk,
        state: dict[str, int],
    ) -> None:
        step = state["step"]

        if not self._window_exists(root):
            return

        if step >= self.config.splash_fade_steps:
            root.attributes("-alpha", 1.0)
            return

        alpha = step / self.config.splash_fade_steps
        root.attributes("-alpha", alpha)
        state["step"] = step + 1

        root.after(
            18,
            lambda: self._fade_in(root, state),
        )

    def _fade_out(
        self,
        root: tk.Tk,
        state: dict[str, int],
    ) -> None:
        state["closing"] = 1
        state["step"] = self.config.splash_fade_steps
        self._fade_out_step(root, state)

    def _fade_out_step(
        self,
        root: tk.Tk,
        state: dict[str, int],
    ) -> None:
        step = state["step"]

        if not self._window_exists(root):
            return

        if step <= 0:
            root.destroy()
            return

        alpha = step / self.config.splash_fade_steps
        root.attributes("-alpha", alpha)
        state["step"] = step - 1

        root.after(
            16,
            lambda: self._fade_out_step(root, state),
        )

    def _animate_loading(
        self,
        canvas: tk.Canvas,
        root: tk.Tk,
        state: dict[str, int],
        theme: Theme,
    ) -> None:
        if state.get("closing") or not self._window_exists(root):
            return

        width, height = self.config.splash_size
        bar_width = 220
        x0 = (width - bar_width) // 2
        y0 = height - 28

        canvas.delete("loader")
        canvas.create_rectangle(
            x0,
            y0,
            x0 + bar_width,
            y0 + 3,
            fill=theme.surface,
            outline=theme.surface,
            tags="loader",
        )

        offset = state["loading"] % bar_width
        canvas.create_rectangle(
            x0 + offset,
            y0,
            x0 + min(offset + 54, bar_width),
            y0 + 3,
            fill=theme.red,
            outline=theme.red,
            tags="loader",
        )
        state["loading"] = offset + 9

        root.after(
            45,
            lambda: self._animate_loading(canvas, root, state, theme),
        )

    def _window_exists(
        self,
        root: tk.Tk,
    ) -> bool:
        try:
            return bool(root.winfo_exists())
        except tk.TclError:
            return False

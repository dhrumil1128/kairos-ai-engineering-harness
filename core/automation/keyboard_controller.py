"""
File: core/automation/keyboard_controller.py

Purpose:
Control keyboard input.

Architecture:

Desktop Agent
      │
KeyboardController
      │
PyAutoGUI
      │
Windows Desktop

Future Roadmap
--------------

V1
- Type text
- Press keys
- Hotkeys

V2
- Key sequences
- Clipboard integration
- Delayed typing

V3
- Human-like typing
- OCR assisted shortcuts
- Macro recording

V4
- Autonomous workflow execution
"""

from __future__ import annotations

from typing import Iterable

import pyautogui


class KeyboardController:
    """
    Production keyboard controller.
    """

    def __init__(self) -> None:
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.05

    def type_text(
        self,
        text: str,
        interval: float = 0.02,
    ) -> str:
        """
        Type text.
        """

        if not isinstance(text, str):
            raise TypeError(
                "text must be a string."
            )

        pyautogui.write(
            text,
            interval=interval,
        )

        return f"Typed: {text}"

    def press_key(
        self,
        key: str,
    ) -> str:
        """
        Press a keyboard key.
        """

        if "+" in key:
            pyautogui.hotkey(*key.split("+"))
        else:
            pyautogui.press(key)

        return f"Pressed: {key}"

    def hotkey(
        self,
        *keys: str,
    ) -> bool:
        """
        Execute keyboard shortcut.
        """

        pyautogui.hotkey(*keys)

        return True

    def key_down(
        self,
        key: str,
    ) -> bool:
        """
        Hold a key.
        """

        pyautogui.keyDown(key)

        return True

    def key_up(
        self,
        key: str,
    ) -> bool:
        """
        Release a key.
        """

        pyautogui.keyUp(key)

        return True

    def press_sequence(
        self,
        keys: Iterable[str],
    ) -> bool:
        """
        Press multiple keys in order.
        """

        for key in keys:
            pyautogui.press(key)

        return True

    def write_multiline(
        self,
        lines: list[str],
        interval: float = 0.02,
    ) -> bool:
        """
        Type multiple lines.
        """

        for line in lines:
            pyautogui.write(
                line,
                interval=interval,
            )
            pyautogui.press("enter")

        return True
"""
File: core/automation/mouse_controller.py

Purpose:
Control the system mouse.

Architecture:

Desktop Agent
      │
MouseController
      │
PyAutoGUI
      │
Windows Desktop

Future Roadmap
--------------

V1
- Mouse movement
- Clicking
- Double clicking
- Position retrieval

V2
- Drag and drop
- Relative movement
- Smooth animation

V3
- OCR assisted targeting
- Vision guided clicks
- Smart object detection

V4
- Autonomous computer interaction
"""

from __future__ import annotations

from typing import Tuple

import pyautogui


class MouseController:
    """
    Production mouse controller.
    """

    def __init__(self) -> None:
        """
        Initialize controller.
        """

        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.05

    def get_position(self) -> Tuple[int, int]:
        """
        Return current mouse position.
        """

        position = pyautogui.position()

        return (
            int(position.x),
            int(position.y),
        )

    def move_mouse(
        self,
        x: int,
        y: int,
        duration: float = 0.2,
    ) -> bool:
        """
        Move cursor to coordinates.
        """

        pyautogui.moveTo(
            x,
            y,
            duration=duration,
        )

        return True

    def move_relative(
        self,
        dx: int,
        dy: int,
        duration: float = 0.2,
    ) -> bool:
        """
        Move relative to current position.
        """

        pyautogui.moveRel(
            dx,
            dy,
            duration=duration,
        )

        return True

    def click(
        self,
        button: str = "left",
    ) -> str:
        """
        Perform a mouse click.
        """

        pyautogui.click(
            button=button,
        )

        return "Click approved"

    def double_click(
        self,
        button: str = "left",
    ) -> bool:
        """
        Double click.
        """

        pyautogui.doubleClick(
            button=button,
        )

        return True

    def right_click(self) -> bool:
        """
        Right click.
        """

        pyautogui.rightClick()

        return True

    def middle_click(self) -> bool:
        """
        Middle click.
        """

        pyautogui.middleClick()

        return True

    def drag_to(
        self,
        x: int,
        y: int,
        duration: float = 0.4,
        button: str = "left",
    ) -> bool:
        """
        Drag cursor.
        """

        pyautogui.dragTo(
            x,
            y,
            duration=duration,
            button=button,
        )

        return True

    def scroll(
        self,
        amount: int,
    ) -> bool:
        """
        Scroll vertically.
        """

        pyautogui.scroll(
            amount,
        )

        return True
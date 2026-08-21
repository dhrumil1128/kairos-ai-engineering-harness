"""
Browser automation controller.

Purpose
-------
Provide generic browser automation
for Chromium and Firefox based browsers.

Architecture

DesktopController
        │
BrowserController
        │
KeyboardController
WindowController
ApplicationController
"""

from __future__ import annotations

import time

from core.automation.application_controller import (
    ApplicationController,
)

from core.automation.keyboard_controller import (
    KeyboardController,
)

from core.automation.window_controller import (
    WindowController,
)


class BrowserController:
    """
    Generic browser automation.
    """

    SUPPORTED_BROWSERS = {
        "chrome",
        "firefox",
        "msedge",
        "edge",
        "brave",
        "opera",
    }

    def __init__(self) -> None:

        self.application = (
            ApplicationController()
        )

        self.keyboard = (
            KeyboardController()
        )

        self.window = (
            WindowController()
        )

        self.active_browser = (
            "chrome"
        )

    # ----------------------------------
    # Browser
    # ----------------------------------

    def open_browser(
        self,
        browser: str = "chrome",
    ) -> bool:
        """
        Open browser.
        """

        browser = browser.lower()

        if browser not in self.SUPPORTED_BROWSERS:

            raise ValueError(
                f"Unsupported browser: {browser}"
            )

        if browser == "edge":
            browser = "msedge"

        self.application.launch(
            browser
        )

        time.sleep(2)

        self.window.focus_window(
            browser
        )

        self.active_browser = (
            browser
        )

        return True

    # ----------------------------------
    # Focus
    # ----------------------------------

    def focus_browser(
        self,
    ) -> bool:
        """
        Focus current browser.
        """

        return self.window.focus_window(
            self.active_browser
        )

    # ----------------------------------
    # Address Bar
    # ----------------------------------

    def focus_address_bar(
        self,
    ) -> bool:
        """
        Focus browser address bar.
        """

        self.focus_browser()

        self.keyboard.hotkey(
            "ctrl",
            "l",
        )

        return True

    # ----------------------------------
    # Navigate
    # ----------------------------------

    def navigate_url(
        self,
        url: str,
    ) -> bool:
        """
        Navigate to URL.
        """

        self.focus_address_bar()

        self.keyboard.type_text(
            url
        )

        self.keyboard.press_key(
            "enter"
        )

        return True

    # ----------------------------------
    # Browser Status
    # ----------------------------------

    def browser(
        self,
    ) -> str:
        """
        Current browser.
        """

        return self.active_browser

    def set_browser(
        self,
        browser: str,
    ) -> bool:
        """
        Set active browser.
        """

        browser = browser.lower()

        if browser == "edge":
            browser = "msedge"

        self.active_browser = browser

        return True

    def browser_running(
        self,
    ) -> bool:
        """
        Check browser status.
        """

        return self.application.is_running(
            self.active_browser
        )
    
        # ----------------------------------
    # Search
    # ----------------------------------

    def search(
        self,
        query: str,
    ) -> bool:
        """
        Search using the browser's
        default search engine.
        """

        self.focus_address_bar()

        self.keyboard.type_text(
            query
        )

        self.keyboard.press_key(
            "enter"
        )

        return True

    # ----------------------------------
    # Tabs
    # ----------------------------------

    def new_tab(
        self,
    ) -> bool:
        """
        Open a new tab.
        """

        self.focus_browser()

        self.keyboard.hotkey(
            "ctrl",
            "t",
        )

        return True

    def close_tab(
        self,
    ) -> bool:
        """
        Close current tab.
        """

        self.focus_browser()

        self.keyboard.hotkey(
            "ctrl",
            "w",
        )

        return True

    def reopen_closed_tab(
        self,
    ) -> bool:
        """
        Reopen last closed tab.
        """

        self.focus_browser()

        self.keyboard.hotkey(
            "ctrl",
            "shift",
            "t",
        )

        return True

    def duplicate_tab(
        self,
    ) -> bool:
        """
        Duplicate current tab.
        """

        self.focus_browser()

        self.keyboard.hotkey(
            "ctrl",
            "l",
        )

        self.keyboard.hotkey(
            "ctrl",
            "c",
        )

        self.new_tab()

        self.keyboard.hotkey(
            "ctrl",
            "v",
        )

        self.keyboard.press_key(
            "enter"
        )

        return True

    def switch_tab(
        self,
        index: int,
    ) -> bool:
        """
        Switch to numbered tab.
        """

        self.focus_browser()

        if index < 1:
            index = 1

        if index > 8:
            index = 8

        self.keyboard.hotkey(
            "ctrl",
            str(index),
        )

        return True

    def next_tab(
        self,
    ) -> bool:
        """
        Switch to next tab.
        """

        self.focus_browser()

        self.keyboard.hotkey(
            "ctrl",
            "tab",
        )

        return True

    def previous_tab(
        self,
    ) -> bool:
        """
        Switch to previous tab.
        """

        self.focus_browser()

        self.keyboard.hotkey(
            "ctrl",
            "shift",
            "tab",
        )

        return True

    # ----------------------------------
    # Navigation
    # ----------------------------------

    def refresh(
        self,
    ) -> bool:
        """
        Refresh current page.
        """

        self.focus_browser()

        self.keyboard.press_key(
            "f5",
        )

        return True

    def hard_refresh(
        self,
    ) -> bool:
        """
        Force refresh.
        """

        self.focus_browser()

        self.keyboard.hotkey(
            "ctrl",
            "f5",
        )

        return True

    def back(
        self,
    ) -> bool:
        """
        Navigate back.
        """

        self.focus_browser()

        self.keyboard.hotkey(
            "alt",
            "left",
        )

        return True

    def forward(
        self,
    ) -> bool:
        """
        Navigate forward.
        """

        self.focus_browser()

        self.keyboard.hotkey(
            "alt",
            "right",
        )

        return True

    def home(
        self,
    ) -> bool:
        """
        Open browser home page.
        """

        self.focus_browser()

        self.keyboard.hotkey(
            "alt",
            "home",
        )

        return True

    # ----------------------------------
    # Browser Pages
    # ----------------------------------

    def downloads(
        self,
    ) -> bool:
        """
        Open downloads.
        """

        self.focus_browser()

        self.keyboard.hotkey(
            "ctrl",
            "j",
        )

        return True

    def history(
        self,
    ) -> bool:
        """
        Open history.
        """

        self.focus_browser()

        self.keyboard.hotkey(
            "ctrl",
            "h",
        )

        return True

    def bookmarks(
        self,
    ) -> bool:
        """
        Open bookmarks.
        """

        self.focus_browser()

        self.keyboard.hotkey(
            "ctrl",
            "shift",
            "b",
        )

        return True
    
        # ----------------------------------
    # Window
    # ----------------------------------

    def fullscreen(
        self,
    ) -> bool:
        """
        Toggle fullscreen.
        """

        self.focus_browser()

        self.keyboard.press_key(
            "f11",
        )

        return True

    def developer_tools(
        self,
    ) -> bool:
        """
        Open Developer Tools.
        """

        self.focus_browser()

        self.keyboard.press_key(
            "f12",
        )

        return True

    def incognito(
        self,
    ) -> bool:
        """
        Open private browsing window.
        """

        self.focus_browser()

        if self.active_browser == "firefox":

            self.keyboard.hotkey(
                "ctrl",
                "shift",
                "p",
            )

        else:

            self.keyboard.hotkey(
                "ctrl",
                "shift",
                "n",
            )

        return True

    # ----------------------------------
    # Zoom
    # ----------------------------------

    def zoom_in(
        self,
    ) -> bool:
        """
        Zoom in.
        """

        self.focus_browser()

        self.keyboard.hotkey(
            "ctrl",
            "+",
        )

        return True

    def zoom_out(
        self,
    ) -> bool:
        """
        Zoom out.
        """

        self.focus_browser()

        self.keyboard.hotkey(
            "ctrl",
            "-",
        )

        return True

    def reset_zoom(
        self,
    ) -> bool:
        """
        Reset page zoom.
        """

        self.focus_browser()

        self.keyboard.hotkey(
            "ctrl",
            "0",
        )

        return True

    # ----------------------------------
    # Scrolling
    # ----------------------------------

    def scroll_up(
        self,
        amount: int = 800,
    ) -> bool:
        """
        Scroll page up.
        """

        self.focus_browser()

        import pyautogui

        pyautogui.scroll(
            amount,
        )

        return True

    def scroll_down(
        self,
        amount: int = 800,
    ) -> bool:
        """
        Scroll page down.
        """

        self.focus_browser()

        import pyautogui

        pyautogui.scroll(
            -amount,
        )

        return True

    def page_top(
        self,
    ) -> bool:
        """
        Go to top of page.
        """

        self.focus_browser()

        self.keyboard.press_key(
            "home",
        )

        return True

    def page_bottom(
        self,
    ) -> bool:
        """
        Go to bottom of page.
        """

        self.focus_browser()

        self.keyboard.press_key(
            "end",
        )

        return True

    # ----------------------------------
    # Page
    # ----------------------------------

    def stop_loading(
        self,
    ) -> bool:
        """
        Stop page loading.
        """

        self.focus_browser()

        self.keyboard.press_key(
            "esc",
        )

        return True

    def find(
        self,
        text: str,
    ) -> bool:
        """
        Find text on page.
        """

        self.focus_browser()

        self.keyboard.hotkey(
            "ctrl",
            "f",
        )

        self.keyboard.type_text(
            text,
        )

        return True

    def save_page(
        self,
    ) -> bool:
        """
        Save current page.
        """

        self.focus_browser()

        self.keyboard.hotkey(
            "ctrl",
            "s",
        )

        return True

    def print_page(
        self,
    ) -> bool:
        """
        Print current page.
        """

        self.focus_browser()

        self.keyboard.hotkey(
            "ctrl",
            "p",
        )

        return True

    def view_source(
        self,
    ) -> bool:
        """
        View page source.
        """

        self.focus_browser()

        self.keyboard.hotkey(
            "ctrl",
            "u",
        )

        return True

    # ----------------------------------
    # Utilities
    # ----------------------------------

    def wait(
        self,
        seconds: float,
    ) -> bool:
        """
        Wait.
        """

        time.sleep(
            seconds,
        )

        return True

    def browser_ready(
        self,
    ) -> bool:
        """
        Check browser availability.
        """

        return (
            self.browser_running()
            and
            self.focus_browser()
        )

    def close_browser(
        self,
    ) -> bool:
        """
        Close browser window.
        """

        self.focus_browser()

        self.keyboard.hotkey(
            "alt",
            "f4",
        )

        return True
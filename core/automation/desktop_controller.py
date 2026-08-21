"""
File: core/automation/desktop_controller.py

Purpose:
Central automation controller.

Architecture:

                Desktop Agent
                      │
             DesktopController
      ┌────────┼────────┬────────┐
      │        │        │        │
Application Window  Mouse  Keyboard
Controller  Controller Controller Controller

Future Roadmap
--------------

V1
- Central automation API
- Controller orchestration

V2
- Task execution
- Workflow engine

V3
- Vision integration
- Browser automation
- Recovery engine

V4
- Autonomous computer use
"""

from __future__ import annotations

from core.automation.application_controller import (
    ApplicationController,
)
from core.automation.window_controller import (
    WindowController,
)
from core.automation.mouse_controller import (
    MouseController,
)
from core.automation.keyboard_controller import (
    KeyboardController,
)

from core.automation.desktop_session_manager import (
    DesktopSessionManager,
)

from core.automation.browser_controller import (
    BrowserController,
)


from core.automation.element_locator import ElementLocator

class DesktopController:
    """
    Main desktop automation controller.
    """

    def __init__(self) -> None:

        self.application = (
            ApplicationController()
        )

        self.window = (
            WindowController()
        )

        self.mouse = (
            MouseController()
        )

        self.keyboard = (
            KeyboardController()
        )
        
        self.browser = BrowserController()
        
        self.session = DesktopSessionManager()
        
        self.browser = BrowserController()
        
        self.element_locator = ElementLocator()

    def get_status(self) -> dict[str, bool]:
        """
        Return automation status.
        """

        return {
    "applications": (
        self.application is not None
    ),
    "windows": (
        self.window is not None
    ),
    "mouse": (
        self.mouse is not None
    ),
    "keyboard": (
        self.keyboard is not None
    ),
    "browser": (
        self.browser is not None
    ),
}

    def launch_application(
        self,
        application: str,
        argument: str | None = None,
    ) -> str:
        """
        Launch an application and
        update the desktop session.
        """

        result = self.application.launch(
            application
        )

        # Bring the application window
        # to the foreground.
        self.window.focus_window(
            application
        )

        # Update session state.
        self.session.set_active_application(
            application
        )

        self.session.set_active_window(
            application
        )

        return result

    def focus_window(
        self,
        title: str,
    ) -> bool:
        """
        Focus a desktop window and
        update the active session.
        """

        success = self.window.focus_window(
            title
        )

        if success:

            self.session.set_active_window(
                title
            )

        return success

    def click(self, target: str | None = None):

        if target is None:
            return self.mouse.click()

        location = self.element_locator.find(target)

        if location is None:
            raise RuntimeError(f"Unable to locate '{target}'")

        return self.mouse.click(location.x, location.y)

    def move_mouse(
        self,
        x: int,
        y: int,
    ) -> bool:
        """
        Move cursor.
        """

        return self.mouse.move_mouse(
            x,
            y,
        )

    def type_text(
        self,
        text: str,
    ) -> str:
        """
        Type text into the
        active application.
        """

        active_window = self.session.get_active_window()

        if active_window:
            self.window.focus_window(
                active_window
            )

        return self.keyboard.type_text(
            text
        )

    def press_key(
        self,
        key: str,
    ) -> str:
        """
        Press a key in the
        active application.
        """

        active_window = (
            self.session.get_active_window()
        )

        if active_window:
            self.window.focus_window(active_window)

        result = self.keyboard.press_key(key)
        
        if key.lower() == "alt+f4":
            previous = self.session.get_active_window()

            if previous:
                self.session.set_previous_window(previous)

            self.session.set_active_window("Close")

        if key.lower() == "ctrl+s":
            self.session.set_active_window("Save As")

        return result
        
        

    def list_processes(
        self,
    ):
        """
        Return running processes.
        """

        return self.application.list_processes()

    def get_windows(
        self,
    ) -> list[str]:
        """
        Return desktop windows.
        """

        return self.window.get_window_titles()

    def get_mouse_position(
        self,
    ) -> tuple[int, int]:
        """
        Return cursor position.
        """

        return self.mouse.get_position()
    
    
    def active_window(
        self,
    ) -> str | None:
        """
        Return active window.
        """

        return self.session.get_active_window()
    
    
    def active_application(
        self,
    ) -> str | None:
        """
        Return active application.
        """

        return self.session.get_active_application()
    

    def double_click(
        self,
    ) -> bool:
        """
        Perform a double click.
        """

        return self.mouse.double_click()
    
    
    
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

        result = self.browser.open_browser(
            browser
        )

        self.session.set_active_application(
            browser
        )

        self.session.set_active_window(
            browser
        )

        return result


    def navigate_url(
        self,
        url: str,
    ) -> bool:
        """
        Navigate browser.
        """

        return self.browser.navigate_url(
            url
        )


    def browser_search(
        self,
        query: str,
    ) -> bool:
        """
        Search using browser.
        """

        return self.browser.search(
            query
        )


    def new_tab(
        self,
    ) -> bool:
        """
        Open browser tab.
        """

        return self.browser.new_tab()


    def close_tab(
        self,
    ) -> bool:
        """
        Close browser tab.
        """

        return self.browser.close_tab()


    def refresh_browser(
        self,
    ) -> bool:
        """
        Refresh browser.
        """

        return self.browser.refresh()


    def browser_back(
        self,
    ) -> bool:
        """
        Browser back.
        """

        return self.browser.back()


    def browser_forward(
        self,
    ) -> bool:
        """
        Browser forward.
        """

        return self.browser.forward()


    def browser_history(
        self,
    ) -> bool:
        """
        Open history.
        """

        return self.browser.history()


    def browser_downloads(
        self,
    ) -> bool:
        """
        Open downloads.
        """

        return self.browser.downloads()


    def close_browser(
        self,
    ) -> bool:
        """
        Close browser.
        """

        return self.browser.close_browser()
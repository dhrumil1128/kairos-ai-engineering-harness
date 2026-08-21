"""
File: core/automation/desktop_session_manager.py

Purpose:
Maintain desktop session state.

Why:

Desktop automation needs
persistent context between
commands.

Examples:

/focus Notepad
/type Hello

The system must remember
which window is active.

Architecture:

Desktop Agent
      ↓
DesktopSessionManager
      ↓
Window State
      ↓
Desktop Actions


Future Roadmap
--------------

V1:
- Track active window.

V2:
- Track active project.
- Track active application.
- Auto restore focus.

V3:
- Screenshot verification.
- Vision assisted targeting.
- Workflow memory.

V4:
- Full autonomous desktop agent.
- Multi application orchestration.
- Enterprise computer use.
"""


class DesktopSessionManager:
    """
    Manage desktop session state.
    """

    def __init__(self):
        """
        Initialize session.
        """

        self.active_window = None
        self.active_application = None
        self.active_project = None
        self.previous_window: str | None = None

    def set_active_window(
        self,
        window_title: str
    ) -> None:
        """
        Store active window.
        """

        self.active_window = window_title

    def get_active_window(
        self
    ) -> str | None:
        """
        Get active window.
        """

        return self.active_window

    def set_active_application(
        self,
        application: str
    ) -> None:
        """
        Store active application.
        """

        self.active_application = application

    def get_active_application(
        self
    ) -> str | None:
        """
        Get active application.
        """

        return self.active_application

    def set_active_project(
        self,
        project: str
    ) -> None:
        """
        Store active project.
        """

        self.active_project = project

    def get_active_project(
        self
    ) -> str | None:
        """
        Get active project.
        """

        return self.active_project
    
    def set_previous_window(self, title: str) -> None:
        self.previous_window = title

    def get_previous_window(self) -> str | None:
        return self.previous_window
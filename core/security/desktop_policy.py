"""
File: core/security/desktop_policy.py

Purpose:
Desktop security policy.

Controls which applications
KAIROS may interact with.

Why:

Desktop automation is powerful.

We do NOT want a restrictive
whitelist because users may
open thousands of different
applications.

Instead we use a security
blocklist approach.

Allow:
- Chrome
- VSCode
- Notepad
- Calculator
- Discord
- Spotify
- Steam
- Any normal user application

Block:
- Dangerous system tools
- Destructive commands
- Administrative utilities

Architecture:

Desktop Agent
      ↓
Desktop Policy
      ↓
Application Controller
      ↓
Operating System

V1:
- Blocklist security

V2:
- User approval prompts

V3:
- Dynamic policy loading

V4:
- Project-level permissions

V5:
- Enterprise policy engine

Enterprise:

- RBAC
- Team policies
- Audit trails
- Approval workflows
"""


class DesktopPolicy:
    """
    Desktop security policy.

    V1 Philosophy:

    Allow most user applications.

    Block only known dangerous
    system utilities.

    This gives Claude-Code style
    flexibility while maintaining
    basic protection.
    """

    def __init__(
        self
    ):
        """
        Initialize policy.
        """

        # -------------------------------------------------
        # Blocked applications.
        #
        # These applications can
        # modify the operating
        # system or execute
        # dangerous actions.
        #
        # V1:
        # Simple blocklist.
        #
        # Enterprise:
        # Dynamic policy engine.
        # -------------------------------------------------

        self.blocked_apps = {

            # Registry editor.
            "regedit",

            # Disk management.
            "diskpart",

            # Local policy editor.
            "gpedit",

            # Services manager.
            "services.msc",

            # Event viewer.
            "eventvwr",

            # Computer management.
            "compmgmt.msc",

            # System configuration.
            "msconfig",

            # Dangerous command patterns.
            "format",
            "shutdown",
            "taskkill",

            # Encoded PowerShell.
            "powershell -enc",

            # Destructive CMD.
            "cmd /c del",
            "cmd /c format"
        }

    def is_allowed(
        self,
        application: str
    ) -> bool:
        """
        Verify application access.

        Returns:

        True
            Safe to launch.

        False
            Blocked by policy.
        """

        app = (
            application
            .strip()
            .lower()
        )

        # -----------------------------------------
        # Block if application matches any
        # dangerous pattern.
        # -----------------------------------------

        for blocked in self.blocked_apps:

            if blocked in app:

                return False

        # -----------------------------------------
        # Everything else is allowed.
        #
        # Examples:
        #
        # chrome
        # vscode
        # calculator
        # spotify
        # discord
        # steam
        # explorer
        # notepad
        # any normal application
        # -----------------------------------------

        return True

    def get_blocked_apps(
        self
    ) -> set[str]:
        """
        Return blocked apps.
        """

        return (
            self.blocked_apps
        )
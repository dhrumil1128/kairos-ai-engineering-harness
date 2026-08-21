"""
File: core/cli/banner.py

Purpose:
Render KAIROS CLI banner.

Why:

Provides a professional
startup experience.

Architecture:

CLI
 ↓
Banner
 ↓
Startup
"""

from rich.panel import Panel
from rich.console import Console


class Banner:
    """
    Render CLI banner.
    """

    def __init__(self):
        """
        Initialize console.
        """

        self.console = Console()

    def render(self) -> str:
        """
        Generate banner text.
        """

        return """
    [bold red]
        KAIROSE

    ██╗  ██╗ █████╗ ██╗██████╗  ██████╗ ███████╗
    ██║ ██╔╝██╔══██╗██║██╔══██╗██╔═══██╗██╔════╝
    █████╔╝ ███████║██║██████╔╝██║   ██║███████╗
    ██╔═██╗ ██╔══██║██║██╔══██╗██║   ██║╚════██║
    ██║  ██╗██║  ██║██║██║  ██║╚██████╔╝███████║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝

    [/bold red]

    [bold white]
    Multi-Agent Intelligence Platform
    [/bold white]
    """

    def display(self) -> None:
        """
        Display banner.
        """

        self.console.print(
            Panel(
                self.render(),
                title="[bold red]KAIROS[/bold red]",
                border_style="red",
                expand=True
            )
        )
"""
Professional KAIROS desktop theme.
"""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtGui import QColor, QFont, QFontDatabase, QPalette
from PySide6.QtWidgets import QApplication


@dataclass(frozen=True)
class DesktopTheme:
    """
    Central color, typography, and stylesheet system.
    """

    background: str = "#000000"
    surface: str = "#000000"
    surface_raised: str = "#111216"
    border: str = "#1F2026"
    red: str = "#E11D2E"
    red_dark: str = "#8A111B"
    text: str = "#F3F4F6"
    muted: str = "#A1A1AA"
    dim: str = "#62626D"
    terminal: str = "#030405"
    terminal_text: str = "#F4F4F5"

    def apply(self, app: QApplication) -> None:
        """
        Apply palette, font, and QSS to the QApplication.
        """

        app.setStyle("Fusion")
        app.setFont(self.application_font())
        app.setPalette(self.palette())
        app.setStyleSheet(self.stylesheet())

    def application_font(self) -> QFont:
        font = QFont("Segoe UI", 10)
        font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        return font

    def mono_font(self) -> QFont:
        families = set(QFontDatabase.families())
        family = "JetBrains Mono" if "JetBrains Mono" in families else "Cascadia Code"
        font = QFont(family, 10)
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setFixedPitch(True)
        return font

    def palette(self) -> QPalette:
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(self.background))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(self.text))
        palette.setColor(QPalette.ColorRole.Base, QColor(self.terminal))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(self.surface))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(self.surface_raised))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(self.text))
        palette.setColor(QPalette.ColorRole.Text, QColor(self.text))
        palette.setColor(QPalette.ColorRole.Button, QColor(self.surface_raised))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(self.text))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(self.red))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#FFFFFF"))
        return palette

    def stylesheet(self) -> str:
        return f"""
        QMainWindow, QWidget {{
            background: {self.background};
            color: {self.text};
        }}

        QLabel {{
            color: {self.text};
            letter-spacing: 0px;
        }}

        QFrame#AppShell {{
            background: {self.background};
        }}

        QFrame#TitleBar {{
            background: #000000;
            border: none;
        }}

        QLabel#TitleLogo {{
            background: transparent;
        }}

        QLabel#TitleText {{
            background: transparent;
            color: {self.text};
            font-size: 15px;
            font-weight: 700;
        }}

        QLabel#RuntimeStatus {{
            background: transparent;
            color: {self.red};
            font-size: 12px;
            font-weight: 600;
        }}

        QPushButton#WindowButton {{
            background: transparent;
            border: none;
            border-radius: 0;
            color: {self.muted};
            font-family: "Segoe MDL2 Assets";
            font-size: 10px;
            font-weight: 400;
            padding: 0;
        }}

        QPushButton#WindowButton:hover {{
            background: #1F2025;
            color: {self.text};
        }}

        QPushButton#WindowButton:pressed {{
            background: #2A2C33;
        }}

        QPushButton#CloseButton {{
            background: transparent;
            border: none;
            border-radius: 0;
            color: {self.muted};
            font-family: "Segoe MDL2 Assets";
            font-size: 10px;
            font-weight: 400;
            padding: 0;
        }}

        QPushButton#CloseButton:hover {{
            background: #C42B1C;
            color: #FFFFFF;
        }}

        QPushButton#CloseButton:pressed {{
            background: #8A1D13;
        }}

        QFrame#TerminalPanel {{
            background: {self.terminal};
            border: none;
            border-radius: 0;
        }}

        QPlainTextEdit#TerminalView {{
            background: {self.terminal};
            color: {self.terminal_text};
            border: none;
            selection-background-color: {self.red_dark};
            selection-color: #FFFFFF;
            padding: 6px 8px 8px 8px;
        }}

        QScrollBar:vertical {{
            background: {self.terminal};
            width: 10px;
            margin: 0;
        }}

        QScrollBar::handle:vertical {{
            background: #353540;
            border-radius: 6px;
            min-height: 32px;
        }}

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {{
            height: 0;
        }}
        """

from core.automation.desktop_session_manager import (
    DesktopSessionManager
)


def test_store_window():

    session = (
        DesktopSessionManager()
    )

    session.set_active_window(
        "Notepad"
    )

    assert (
        session.get_active_window()
        == "Notepad"
    )


def test_store_application():

    session = (
        DesktopSessionManager()
    )

    session.set_active_application(
        "VS Code"
    )

    assert (
        session.get_active_application()
        == "VS Code"
    )


def test_store_project():

    session = (
        DesktopSessionManager()
    )

    session.set_active_project(
        "E:\\KAIROS"
    )

    assert (
        session.get_active_project()
        == "E:\\KAIROS"
    )
"""
Tests for core.python.module_discovery.

Purpose:
Verify that discover_generated_modules() correctly identifies
generated Python packages and modules.

These tests define the expected behaviour of the module discovery
engine used throughout KAIROS.
"""

from core.python.module_discovery import discover_generated_modules


def test_empty_input_returns_empty_set():
    assert discover_generated_modules([]) == set()


def test_ignores_non_python_files():
    paths = [
        "README.md",
        "requirements.txt",
        ".gitignore",
        "docs/architecture.md",
    ]

    assert discover_generated_modules(paths) == set()


def test_discovers_src_project():
    paths = [
        "src/main.py",
    ]

    assert discover_generated_modules(paths) == {
        "src",
        "main",
    }


def test_discovers_package():
    paths = [
        "hello_world/__init__.py",
        "hello_world/hello_world.py",
    ]

    assert discover_generated_modules(paths) == {
        "hello_world",
    }


def test_discovers_nested_packages():
    paths = [
        "backend/api/routes.py",
    ]

    assert discover_generated_modules(paths) == {
        "backend",
        "api",
        "routes",
    }


def test_discovers_multiple_packages():
    paths = [
        "src/main.py",
        "hello_world/__init__.py",
        "hello_world/utils.py",
        "tests/test_main.py",
    ]

    assert discover_generated_modules(paths) == {
        "src",
        "main",
        "hello_world",
        "utils",
        "tests",
        "test_main",
    }


def test_handles_windows_paths():
    paths = [
        r"src\main.py",
        r"package\__init__.py",
        r"package\helpers.py",
    ]

    assert discover_generated_modules(paths) == {
        "src",
        "main",
        "package",
        "helpers",
    }


def test_duplicate_files_do_not_create_duplicate_modules():
    paths = [
        "src/main.py",
        "src/main.py",
        "src/main.py",
    ]

    assert discover_generated_modules(paths) == {
        "src",
        "main",
    }


def test_nested_module_structure():
    paths = [
        "app/services/auth.py",
        "app/services/database.py",
        "app/models/user.py",
    ]

    assert discover_generated_modules(paths) == {
        "app",
        "services",
        "auth",
        "database",
        "models",
        "user",
    } 
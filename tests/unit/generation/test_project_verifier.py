from pathlib import Path

import pytest

from core.generation.project_verifier import ProjectVerifier


def write(path: Path, content: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


@pytest.fixture
def verifier():
    return ProjectVerifier()


def test_generated_modules_detects_src_package(tmp_path: Path, verifier):
    """
    src/main.py
        -> src
        -> main
    """

    write(tmp_path / "src" / "main.py")

    modules = verifier._generated_modules(tmp_path)

    assert "src" in modules
    assert "main" in modules


def test_generated_modules_detects_nested_packages(tmp_path: Path, verifier):
    """
    package/utils/helper.py
        -> package
        -> utils
        -> helper
    """

    write(tmp_path / "package" / "utils" / "helper.py")

    modules = verifier._generated_modules(tmp_path)

    assert modules == {"package", "helper"}
    


def test_generated_modules_detects_package_from_init(tmp_path: Path, verifier):
    """
    hello_world/
        __init__.py
    """

    write(tmp_path / "hello_world" / "__init__.py")

    modules = verifier._generated_modules(tmp_path)

    assert "hello_world" in modules


def test_generated_modules_detects_multiple_packages(tmp_path: Path, verifier):
    write(tmp_path / "src" / "main.py")
    write(tmp_path / "tests" / "test_main.py")
    write(tmp_path / "core" / "__init__.py")
    write(tmp_path / "core" / "engine.py")

    modules = verifier._generated_modules(tmp_path)

    expected = {
        "src",
        "main",
        "tests",
        "test_main",
        "core",
        "engine",
    }

    assert expected.issubset(modules)


def test_generated_modules_ignores_non_python_files(tmp_path: Path, verifier):
    write(tmp_path / "README.md")
    write(tmp_path / "config.json")
    write(tmp_path / "src" / "main.py")

    modules = verifier._generated_modules(tmp_path)

    assert "README" not in modules
    assert "config" not in modules
    assert "src" in modules
    assert "main" in modules


def test_generated_modules_empty_project(tmp_path: Path, verifier):
    modules = verifier._generated_modules(tmp_path)

    assert modules == set()
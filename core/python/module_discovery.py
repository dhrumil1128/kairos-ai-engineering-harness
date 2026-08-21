"""
File:
core/python/module_discovery.py

Purpose:
Discover every generated Python module and package
within a generated KAIROS project.

Why:

Multiple KAIROS components need to know which
Python modules belong to the generated project.

Instead of duplicating module discovery logic,
this module provides a single source of truth.

Used By:

- ProjectVerifier
- GenerationPipeline
- Future Dependency Analyzer
- Future Refactoring Engine

Responsibilities:

- Discover generated Python packages.
- Discover generated Python modules.
- Ignore non-Python files.
- Return a unique collection of module names.

Does NOT:

- Read files from disk.
- Parse Python source.
- Validate imports.
- Generate requirements.
- Execute code.
"""

from __future__ import annotations

from pathlib import PurePosixPath
from typing import Iterable


def discover_generated_modules(
    paths: Iterable[str],
) -> set[str]:
    """
    Discover generated Python modules and packages.

    Parameters
    ----------
    paths:
        Iterable containing generated project file paths.

    Returns
    -------
    set[str]

        Examples

        src/main.py
            -> src
            -> main

        package/__init__.py
            -> package

        package/utils/helper.py
            -> package
            -> utils
            -> helper
    """

    modules: set[str] = set()

    for raw_path in paths:

        path = str(raw_path).replace("\\", "/").strip()

        if not path.endswith(".py"):
            continue

        parts = PurePosixPath(path).parts

        if not parts:
            continue

        # Every directory is considered a generated package.
        for directory in parts[:-1]:
            if directory:
                modules.add(directory)

        filename = parts[-1]

        # __init__.py represents the package itself.
        if filename == "__init__.py":
            continue

        module_name = filename[:-3]

        if module_name:
            modules.add(module_name)

    return modules
from __future__ import annotations

from pathlib import Path, PureWindowsPath


def is_absolute_path(path: str) -> bool:
    return (
        Path(path).is_absolute()
        or PureWindowsPath(path).is_absolute()
    )


def resolve_output_path(
    project_root: str,
    *parts: str,
) -> str:
    if not parts:
        return str(Path(project_root))

    first_part = str(parts[0])

    if is_absolute_path(first_part):
        return str(Path(first_part).joinpath(*parts[1:]))

    return str(Path(project_root).joinpath(*parts))

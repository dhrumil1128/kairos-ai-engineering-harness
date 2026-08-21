from dataclasses import dataclass


@dataclass(slots=True)
class FileState:

    path: str

    content: str = ""

    symbols: dict | None = None

    generated: bool = False
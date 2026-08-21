from dataclasses import dataclass


@dataclass
class RepositoryContext:
    language: str | None = None
    framework: str | None = None
    project_type: str | None = None
    has_git: bool = False
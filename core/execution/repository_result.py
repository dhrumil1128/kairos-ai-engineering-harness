from dataclasses import dataclass
from pathlib import Path


@dataclass
class RepositoryResult:
    repository_path: Path | None = None
    repository_name: str | None = None
    is_git_repository: bool = False
    language: str | None = None
    framework: str | None = None
    project_type: str | None = None
    build_system: str | None = None
    dependency_manager: str | None = None
    source_directory: str | None = None
    entry_point: str | None = None
    documentation: list[str] | None = None
    license_file: str | None = None
    containerized: bool = False
    ci_cd: bool = False
    testing_framework: str | None = None
    virtual_environment: bool = False

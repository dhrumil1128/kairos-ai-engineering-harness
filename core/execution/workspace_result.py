from dataclasses import dataclass


@dataclass
class WorkspaceResult:
    exists: bool
    is_empty: bool
    path: str
    is_git_repository: bool = False
    file_count: int = 0
    directory_count: int = 0
    project_markers: list[str] | None = None
    is_existing_project: bool = False

    @property
    def workspace(self) -> str:
        return self.path

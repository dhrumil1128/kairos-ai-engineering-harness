from dataclasses import dataclass


@dataclass
class WorkspaceContext:
    path: str
    exists: bool = False
    is_empty: bool = False
    is_git_repository: bool = False
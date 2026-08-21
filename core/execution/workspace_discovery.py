"""
Workspace discovery module.

Responsible for discovering the current workspace before the
execution engine begins processing.

Responsibilities:
- Validate workspace
- Collect basic workspace information
- Detect project markers
- Detect Git repository

This module DOES NOT:
- Analyze source code
- Build execution plans
- Call AI models
- Modify files
"""

from __future__ import annotations

from pathlib import Path

from .workspace_result import WorkspaceResult


class WorkspaceDiscovery:
    """
    Discovers basic information about a workspace.

    This class is the first stage of the KAIROS Execution Engine
    and only performs filesystem discovery.
    """

    PROJECT_MARKERS: tuple[str, ...] = (
        "pyproject.toml",
        "requirements.txt",
        "setup.py",
        "setup.cfg",
        "Pipfile",
        "poetry.lock",
        "package.json",
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        "Cargo.toml",
        "go.mod",
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
        "composer.json",
        ".gitignore",
        "README.md",
        "README.rst",
        "README.txt",
    )

    def discover(self, workspace: str) -> WorkspaceResult:
        """
        Discover the workspace.

        Parameters
        ----------
        workspace:
            Path to the workspace.

        Returns
        -------
        WorkspaceResult
            Basic workspace information.
        """

        workspace_path = self._validate_workspace(workspace)

        exists = workspace_path.exists()

        if not exists:
            return WorkspaceResult(
                exists=False,
                is_empty=True,
                path=str(workspace_path),
                is_git_repository=False,
            )
            
        # ADD THIS HERE
        if not workspace_path.is_dir():
            raise NotADirectoryError(
                f"'{workspace_path}' is not a directory."
            )
            
        

        is_empty = self._is_empty(workspace_path)
        is_git_repository = self._is_git_repository(workspace_path)

        file_count = self._count_files(workspace_path)
        directory_count = self._count_directories(workspace_path)

        project_markers = self._detect_project_markers(workspace_path)

        

        return self._build_result(
            workspace=workspace_path,
            exists=True,
            is_empty=is_empty,
            is_git_repository=is_git_repository,
            file_count=file_count,
            directory_count=directory_count,
            project_markers=project_markers,
        )
                
    
    def _validate_workspace(self, workspace: str) -> Path:
        """
        Validate and normalize the workspace path.
        """

        if not workspace or not workspace.strip():
            raise ValueError("Workspace path cannot be empty.")

        try:
            return Path(workspace).expanduser().resolve()
        except Exception as exc:
            raise ValueError(f"Invalid workspace path: {workspace}") from exc

    def _is_empty(self, workspace: Path) -> bool:
        """
        Check whether the workspace is empty.
        """

        try:
            return not any(workspace.iterdir())
        except PermissionError as exc:
            raise PermissionError(
                f"Permission denied while accessing '{workspace}'."
            ) from exc

    def _is_git_repository(self, workspace: Path) -> bool:
        """
        Determine whether the workspace is a Git repository.
        """

        return (workspace / ".git").is_dir()

    def _count_files(self, workspace: Path) -> int:
        """
        Count all files inside the workspace.
        """

        count = 0

        try:
            for path in workspace.rglob("*"):
                try:
                    if path.is_file():
                        count += 1
                except (PermissionError, OSError):
                    continue
        except (PermissionError, OSError):
            return count

  

    def _count_directories(self, workspace: Path) -> int:
        """
        Count all directories inside the workspace.
        """

        count = 0

        try:
            for path in workspace.rglob("*"):
                try:
                    if path.is_dir():
                        count += 1
                except (PermissionError, OSError):
                    continue
        except (PermissionError, OSError):
            return count

        return count

    def _detect_project_markers(self, workspace: Path) -> list[str]:
        """
        Detect common project marker files.
        """

        markers: list[str] = []

        for marker in self.PROJECT_MARKERS:
            if (workspace / marker).exists():
                markers.append(marker)

        return sorted(markers)
    
    
  

    def _workspace_exists(self, workspace: Path) -> bool:
        """
        Check whether the workspace exists.
        """

        return workspace.exists()

    def _is_directory(self, workspace: Path) -> bool:
        """
        Check whether the workspace is a directory.
        """

        return workspace.is_dir()

    def _is_existing_project(self, markers: list[str]) -> bool:
        """
        Determine whether this workspace already contains
        a software project.
        """

        return bool(markers)

    def _build_result(
        self,
        workspace: Path,
        *,
        exists: bool,
        is_empty: bool,
        is_git_repository: bool,
        file_count: int,
        directory_count: int,
        project_markers: list[str],
    ) -> WorkspaceResult:
        """
        Construct the final WorkspaceResult.
        """

        return WorkspaceResult(
            exists=exists,
            is_empty=is_empty,
            path=str(workspace),
            is_git_repository=is_git_repository,
            file_count=file_count,
            directory_count=directory_count,
            project_markers=project_markers,
            is_existing_project=self._is_existing_project(project_markers),
        )
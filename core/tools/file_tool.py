"""
File: core/tools/file_tool.py

Purpose:
File operations for KAIROS.

Capabilities:

- Read files
- Write files
- Check existence
- Delete files

Future Versions:

V2:
- Directory listing

V3:
- Recursive search

V4:
- File metadata

V5:
- Workspace sandboxing
"""

import re
import shutil
from pathlib import Path, PureWindowsPath


class FileTool:
    """
    File operations tool.
    """

    WORKSPACE_ROOT = Path("workspace")

    def resolve_path(
        self,
        path: str,
    ) -> Path:
        """
        Resolve filesystem targets.

        Absolute paths are used as-is. Relative paths are scoped to the
        workspace directory. Legacy RouteExecutor values such as
        workspace/D:\\Jarvis are corrected back to D:\\Jarvis.
        """

        raw_path = str(path).strip()
        raw_path = self._remove_workspace_prefix_from_absolute(raw_path)
        candidate = Path(raw_path).expanduser()

        if candidate.is_absolute() or PureWindowsPath(raw_path).is_absolute():
            return candidate

        if candidate.parts and candidate.parts[0].lower() == "workspace":
            return candidate

        return self.WORKSPACE_ROOT / candidate

    def _remove_workspace_prefix_from_absolute(
        self,
        path: str,
    ) -> str:
        match = re.match(
            r"^(?:\.?[\\/])?workspace[\\/]+([A-Za-z]:[\\/].*)$",
            path,
        )

        if match:
            return match.group(1)

        return path

    def read_file(
        self,
        path: str
    ) -> str:
        """
        Read file content.
        """

        return self.resolve_path(
            path
        ).read_text(
            encoding="utf-8"
        )

    def write_file(
        self,
        path: str,
        content: str
    ) -> None:
        """
        Write file content.
        """

        file_path = self.resolve_path(
            path
        )
        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        file_path.write_text(
            content,
            encoding="utf-8"
        )

    def exists(
        self,
        path: str
    ) -> bool:
        """
        Check existence.
        """

        return self.resolve_path(
            path
        ).exists()

    def delete_file(
        self,
        path: str
    ) -> None:
        """
        Delete file.
        """

        file_path = self.resolve_path(path)

        if file_path.exists():
            file_path.unlink()

    def delete_path(
        self,
        path: str
    ) -> None:
        """
        Delete a file or directory.
        """

        target_path = self.resolve_path(path)

        if target_path.is_dir():
            shutil.rmtree(target_path)
            return

        if target_path.exists():
            target_path.unlink()
            
            
            
    # Create directory.
    def create_directory(
        self,
        path: str
    ) -> None:
        """
        Create directory.
        """

        self.resolve_path(
            path
        ).mkdir(
            parents=True,
            exist_ok=True
        )

    def delete_directory(
        self,
        path: str
    ) -> None:
        """
        Delete directory.
        """

        directory_path = self.resolve_path(path)

        if directory_path.exists():
            shutil.rmtree(directory_path)

    def create_file(
        self,
        path: str,
        content: str = ""
    ) -> None:
        """
        Create file.
        """

        self.write_file(path, content)

    def move_file(
        self,
        source: str,
        destination: str
    ) -> None:
        """
        Move file or directory.
        """

        destination_path = self.resolve_path(destination)
        destination_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        shutil.move(
            str(self.resolve_path(source)),
            str(destination_path),
        )

    def copy_file(
        self,
        source: str,
        destination: str
    ) -> None:
        """
        Copy file or directory.
        """

        source_path = self.resolve_path(source)
        destination_path = self.resolve_path(destination)
        destination_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if source_path.is_dir():
            shutil.copytree(
                source_path,
                destination_path,
                dirs_exist_ok=True,
            )
            return

        shutil.copy2(
            source_path,
            destination_path,
        )

    def rename_file(
        self,
        source: str,
        destination: str
    ) -> None:
        """
        Rename file or directory.
        """

        self.move_file(source, destination)
    
    
    # List directory contents.
    def list_directory(
        self,
        path: str
    ) -> list[str]:
        """
        List directory contents.
        """

        return [
            item.name
            for item in self.resolve_path(
                path
            ).iterdir()
        ]
        
    
    # Initialize KAIROS project.
    def create_kairos_project(
        self,
        root_path: str
    ) -> None:
        """
        Create KAIROS memory.
        """

        kairos_dir = (
            self.resolve_path(
                root_path
            )
            / ".kairos"
        )

        kairos_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        files = {
            "architecture.md":
                "# Architecture\n",

            "roadmap.md":
                "# Roadmap\n",

            "coding_standards.md":
                "# Coding Standards\n",

            "project_context.md":
                "# Project Context\n",

            "memory.md":
                "# Memory\n",
        }

        for name, content in (
            files.items()
        ):

            (
                kairos_dir / name
            ).write_text(
                content,
                encoding="utf-8"
            )
            
    
    
    def prepare_project_directory(
        self,
        target_path: str
    ) -> Path:
        """
        Validate and prepare
        the target project
        directory.

        Rules:

        - Parent directory
        must already exist.
        - Project directory
        is created
        automatically.
        """

        project_path = self.resolve_path(
            target_path
        ).resolve()

        parent = project_path.parent

        if not parent.exists():

            raise FileNotFoundError(

                f"Parent directory does not exist:\n{parent}"

            )

        project_path.mkdir(
            exist_ok=True
        )

        return project_path

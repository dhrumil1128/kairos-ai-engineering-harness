"""
File: core/context/project_path_resolver.py

Purpose:
Resolve the target
project directory.

Why:

Allows KAIROS to work
with any local project
instead of relying on
hardcoded paths.

Architecture:

User Prompt
      │
      ▼
Project Path Resolver
      │
      ├── Explicit Path
      ├── Current Directory
      ├── Git Repository
      └── Default Workspace
"""

from __future__ import annotations

import os
import re

from core.logging.kairos_logger import (
    KairosLogger
)


class ProjectPathResolver:
    """
    Resolve project paths
    from user prompts.
    """

    def __init__(
        self
    ):
        """
        Initialize resolver.
        """

        self.logger = (
            KairosLogger(
                "context"
            )
        )

        self.default_project = (
            "workspace/generated_project"
        )
        
        # ---------------------------------- #
    # Resolve Project
    # ---------------------------------- #

    def resolve(
        self,
        command: str
    ) -> str:
        """
        Resolve the project
        directory from the
        user command.
        """

        # ----------------------------------
        # Explicit Windows path
        # ----------------------------------

        match = re.search(
            r"[A-Za-z]:\\[^\r\n]+",
            command
        )

        if match:

            project_path = os.path.abspath(
                match.group(0).strip()
            )

            self.logger.info(
                f"Using target project: {project_path}"
            )

            return project_path

        # ----------------------------------
        # Existing Project
        # ----------------------------------

        current = os.getcwd()

        if os.path.isdir(current):

            self.logger.info(
                f"Using current directory: {current}"
            )

            return current

        # ----------------------------------
        # Default Workspace
        # ----------------------------------

        self.logger.info(
            "Using default workspace."
        )

        return self.default_project
        
    # ---------------------------------- #
    # Git Repository Root
    # ---------------------------------- #

    def repository_root(
        self,
        path: str
    ) -> str:
        """
        Return the Git
        repository root
        if available.
        """

        current = (
            os.path.abspath(
                path
            )
        )

        while True:

            git_dir = os.path.join(
                current,
                ".git"
            )

            if os.path.isdir(
                git_dir
            ):

                self.logger.info(
                    f"Git repository detected: {current}"
                )

                return current

            parent = os.path.dirname(
                current
            )

            if parent == current:

                break

            current = parent

        return path

    # ---------------------------------- #
    # Validate Project
    # ---------------------------------- #

    def validate(
        self,
        path: str
    ) -> bool:
        """
        Validate the
        project path.
        """

        return os.path.isdir(
            path
        )
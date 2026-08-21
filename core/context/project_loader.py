"""
File: core/context/project_loader.py

Purpose:
Load and analyze enterprise
projects for the KAIROS
Context Intelligence Engine.

Why:

Before any agent starts,
KAIROS should understand
the project structure,
framework, languages,
dependencies, entry points,
and context documents.

Architecture:

Project
    │
    ▼
Project Loader
    │
    ├── Project Scan
    ├── Context Discovery
    ├── Language Detection
    ├── Framework Detection
    ├── Entry Point Detection
    ├── Metadata Generation
    │
    ▼
Knowledge Manager

V2:
- Recursive dependency discovery

V3:
- Semantic project analysis

V4:
- Incremental project updates

V5:
- Distributed project indexing
"""

from __future__ import annotations

from pathlib import Path

from core.logging.kairos_logger import (
    KairosLogger,
)


class ProjectLoader:
    """
    Enterprise Project Loader.
    """

    # ---------------------------------- #
    # Supported Context Documents
    # ---------------------------------- #

    CONTEXT_FILES = [

        "README.md",
        "PROJECT.md",
        "PROJECT_CONTEXT.md",

        "ARCHITECTURE.md",
        "API.md",

        "ROADMAP.md",
        "CHANGELOG.md",

        "MEMORY.md",
        "TASKS.md",

        "AGENTS.md",
        "RULES.md",

        "SECURITY.md",

        "DECISIONS.md",

        "STANDARDS.md",

        "COMPLIANCE.md",

        "KNOWLEDGE_BASE.md",
    ]

    # ---------------------------------- #
    # Ignore Directories
    # ---------------------------------- #

    IGNORE_DIRECTORIES = {

        ".git",

        ".venv",

        "venv",

        "__pycache__",

        ".pytest_cache",

        ".mypy_cache",

        ".idea",

        ".vscode",

        "node_modules",

        "dist",

        "build",

        ".kairos",

    }

    # ---------------------------------- #
    # Supported Languages
    # ---------------------------------- #

    LANGUAGE_EXTENSIONS = {

        ".py": "Python",

        ".js": "JavaScript",

        ".ts": "TypeScript",

        ".java": "Java",

        ".cpp": "C++",

        ".c": "C",

        ".cs": "C#",

        ".go": "Go",

        ".rs": "Rust",

        ".php": "PHP",

        ".rb": "Ruby",

        ".swift": "Swift",

        ".kt": "Kotlin",

        ".html": "HTML",

        ".css": "CSS",

    }

    def __init__(
        self
    ):
        """
        Initialize loader.
        """

        self.logger = (
            KairosLogger(
                "context"
            )
        )

    # ---------------------------------- #
    # Load Project
    # ---------------------------------- #

    def load_project(
        self,
        project_path: str
    ) -> dict:
        """
        Load entire project.
        """

        self.logger.info(
            "Project loading started."
        )

        root = Path(
            project_path
        )

        metadata = {

            "root": str(root),

            "documents": {},

            "languages": set(),

            "framework": "Unknown",

            "entrypoints": [],

            "files": [],

            "directories": [],

        }

        self._scan_project(
            root,
            metadata
        )

        metadata[
            "framework"
        ] = self._detect_framework(
            root
        )

        metadata[
            "languages"
        ] = sorted(
            metadata[
                "languages"
            ]
        )

        self.logger.success(
            "Project loading completed."
        )

        return metadata


    # ---------------------------------- #
    # Scan Project
    # ---------------------------------- #

    def _scan_project(
        self,
        directory: Path,
        metadata: dict
    ) -> None:
        """
        Recursively scan
        the project.
        """

        self.logger.info(
            f"Scanning: {directory}"
        )

        for item in directory.iterdir():

            # Ignore hidden folders
            # and build artifacts.

            if (
                item.is_dir()
                and item.name
                in self.IGNORE_DIRECTORIES
            ):
                continue

            if item.is_dir():

                metadata[
                    "directories"
                ].append(
                    str(item)
                )

                self._scan_project(
                    item,
                    metadata
                )

                continue

            metadata[
                "files"
            ].append(
                str(item)
            )

            # -------------------------- #
            # Context Documents
            # -------------------------- #

            if (
                item.name
                in self.CONTEXT_FILES
            ):

                try:

                    metadata[
                        "documents"
                    ][
                        item.name
                    ] = (
                        item.read_text(
                            encoding="utf-8"
                        )
                    )

                    self.logger.info(
                        f"Loaded context: {item.name}"
                    )

                except Exception as error:

                    self.logger.warning(
                        f"Unable to read "
                        f"{item.name}: "
                        f"{error}"
                    )

            # -------------------------- #
            # Language Detection
            # -------------------------- #

            extension = (
                item.suffix.lower()
            )

            if (
                extension
                in self.LANGUAGE_EXTENSIONS
            ):

                metadata[
                    "languages"
                ].add(

                    self
                    .LANGUAGE_EXTENSIONS[
                        extension
                    ]

                )

            # -------------------------- #
            # Entry Point Detection
            # -------------------------- #

            if item.name in [

                "main.py",

                "app.py",

                "server.py",

                "manage.py",

                "index.js",

                "main.ts",

            ]:

                metadata[
                    "entrypoints"
                ].append(
                    str(item)
                )

    # ---------------------------------- #
    # Framework Detection
    # ---------------------------------- #

    def _detect_framework(
        self,
        project_root: Path
    ) -> str:
        """
        Detect the primary
        project framework.
        """

        self.logger.info(
            "Detecting framework."
        )

        # -------------------------- #
        # Python Frameworks
        # -------------------------- #

        requirements = (
            project_root
            / "requirements.txt"
        )

        if requirements.exists():

            content = (
                requirements
                .read_text(
                    encoding="utf-8"
                )
                .lower()
            )

            if "fastapi" in content:
                return "FastAPI"

            if "flask" in content:
                return "Flask"

            if "django" in content:
                return "Django"

            if "streamlit" in content:
                return "Streamlit"

            if "gradio" in content:
                return "Gradio"
        
        # -------------------------- #
        # Node.js Frameworks
        # -------------------------- #

        package_json = (
            project_root
            / "package.json"
        )

        if package_json.exists():

            content = (
                package_json
                .read_text(
                    encoding="utf-8"
                )
                .lower()
            )

            if "next" in content:
                return "Next.js"

            if "react" in content:
                return "React"

            if "vue" in content:
                return "Vue"

            if "angular" in content:
                return "Angular"

            if "express" in content:
                return "Express.js"

        # -------------------------- #
        # Java Frameworks
        # -------------------------- #

        pom_xml = (
            project_root
            / "pom.xml"
        )

        if pom_xml.exists():

            content = (
                pom_xml
                .read_text(
                    encoding="utf-8"
                )
                .lower()
            )

            if "spring-boot" in content:
                return "Spring Boot"

        # -------------------------- #
        # Rust
        # -------------------------- #

        cargo = (
            project_root
            / "cargo.toml"
        )

        if cargo.exists():
            return "Rust"

        # -------------------------- #
        # Go
        # -------------------------- #

        go_mod = (
            project_root
            / "go.mod"
        )

        if go_mod.exists():
            return "Go"

        return "Unknown"

    # ---------------------------------- #
    # Supported Context Files
    # ---------------------------------- #

    def expected_files(
        self
    ) -> list[str]:
        """
        Return supported
        context documents.
        """

        return (
            self.CONTEXT_FILES
            .copy()
        )

    # ---------------------------------- #
    # Supported Languages
    # ---------------------------------- #

    def supported_languages(
        self
    ) -> dict[str, str]:
        """
        Return supported
        language mapping.
        """

        return (
            self.LANGUAGE_EXTENSIONS
            .copy()
        )

    # ---------------------------------- #
    # Ignored Directories
    # ---------------------------------- #

    def ignored_directories(
        self
    ) -> set[str]:
        """
        Return ignored
        directories.
        """

        return (
            self.IGNORE_DIRECTORIES
            .copy()
        )
        
    
    # ---------------------------------- #
    # Project Statistics
    # ---------------------------------- #

    def project_statistics(
        self,
        metadata: dict
    ) -> dict:
        """
        Return project
        statistics.
        """

        return {

            "total_files": len(
                metadata.get(
                    "files",
                    []
                )
            ),

            "total_directories": len(
                metadata.get(
                    "directories",
                    []
                )
            ),

            "total_documents": len(
                metadata.get(
                    "documents",
                    {}
                )
            ),

            "languages": len(
                metadata.get(
                    "languages",
                    []
                )
            ),

            "framework": metadata.get(
                "framework",
                "Unknown"
            ),

            "entrypoints": len(
                metadata.get(
                    "entrypoints",
                    []
                )
            ),

        }

    # ---------------------------------- #
    # Project Summary
    # ---------------------------------- #

    def project_summary(
        self,
        metadata: dict
    ) -> str:
        """
        Generate project
        summary.
        """

        stats = (
            self.project_statistics(
                metadata
            )
        )

        return (
            f"Framework: "
            f"{stats['framework']}\n"
            f"Languages: "
            f"{', '.join(metadata['languages'])}\n"
            f"Files: "
            f"{stats['total_files']}\n"
            f"Directories: "
            f"{stats['total_directories']}\n"
            f"Context Documents: "
            f"{stats['total_documents']}\n"
            f"Entry Points: "
            f"{stats['entrypoints']}"
        )

    # ---------------------------------- #
    # Validation
    # ---------------------------------- #

    def validate_project(
        self,
        project_path: str
    ) -> bool:
        """
        Validate project
        path.
        """

        root = Path(
            project_path
        )

        if (
            not root.exists()
        ):
            return False

        if (
            not root.is_dir()
        ):
            return False

        return True
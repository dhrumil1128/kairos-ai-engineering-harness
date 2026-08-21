"""
Repository Understanding Module.

Analyzes an existing software repository and extracts the
high-level information required by the KAIROS execution engine.

Responsibilities
----------------
- Validate repository
- Detect repository characteristics
- Detect language
- Detect framework
- Detect project type
- Detect build system
- Detect dependency manager
- Detect source directory
- Detect entry point
- Detect documentation
- Detect license
- Detect containerization
- Detect CI/CD
- Detect testing framework

This module NEVER:

- Executes project code
- Installs dependencies
- Modifies repository files
- Generates execution plans
- Calls an LLM
"""

from __future__ import annotations

from pathlib import Path

from .repository_result import RepositoryResult


class RepositoryUnderstanding:
    """
    Understand an existing repository.

    This component is responsible for inspecting a project and
    extracting repository metadata used by later execution stages.
    """

    LANGUAGE_MARKERS = {
        "Python": (
            "pyproject.toml",
            "requirements.txt",
            "setup.py",
            "setup.cfg",
            "Pipfile",
            "poetry.lock",
        ),
        "JavaScript": (
            "package.json",
            "package-lock.json",
            "yarn.lock",
            "pnpm-lock.yaml",
        ),
        "TypeScript": (
            "tsconfig.json",
        ),
        "Java": (
            "pom.xml",
            "build.gradle",
            "build.gradle.kts",
        ),
        "Go": (
            "go.mod",
        ),
        "Rust": (
            "Cargo.toml",
        ),
        "PHP": (
            "composer.json",
        ),
        "C#": (
            "*.csproj",
            "*.sln",
        ),
        "C/C++": (
            "CMakeLists.txt",
            "Makefile",
        ),
    }

    FRAMEWORK_MARKERS = {
        "Django": ("manage.py",),
        "Flask": ("app.py",),
        "FastAPI": ("main.py",),
        "Streamlit": ("streamlit_app.py",),
        "React": ("package.json",),
        "Next.js": (
            "next.config.js",
            "next.config.ts",
        ),
        "Vue": ("vue.config.js",),
        "Angular": ("angular.json",),
        "Express": ("package.json",),
        "Spring Boot": (
            "pom.xml",
            "build.gradle",
        ),
        "Laravel": ("artisan",),
    }

    BUILD_SYSTEMS = {
        "Poetry": "poetry.lock",
        "Pip": "requirements.txt",
        "npm": "package-lock.json",
        "Yarn": "yarn.lock",
        "pnpm": "pnpm-lock.yaml",
        "Cargo": "Cargo.toml",
        "Gradle": "build.gradle",
        "Maven": "pom.xml",
        "CMake": "CMakeLists.txt",
        "Make": "Makefile",
    }

    SOURCE_DIRECTORIES = (
        "src",
        "app",
        "backend",
        "frontend",
        "server",
        "client",
        "lib",
        "services",
    )

    ENTRY_POINTS = (
        "main.py",
        "app.py",
        "server.py",
        "manage.py",
        "index.js",
        "index.ts",
        "main.go",
        "main.rs",
        "Program.cs",
    )

    DOCUMENTATION_FILES = (
        "README.md",
        "README.rst",
        "README.txt",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
    )

    LICENSE_FILES = (
        "LICENSE",
        "LICENSE.md",
        "LICENSE.txt",
    )

    CONTAINER_FILES = (
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.yaml",
    )

    CI_CD_FILES = (
        ".gitlab-ci.yml",
        "azure-pipelines.yml",
        "Jenkinsfile",
    )

    TEST_FRAMEWORKS = {
        "pytest": (
            "pytest.ini",
            "conftest.py",
        ),
        "unittest": (
            "unittest.cfg",
        ),
        "Jest": (
            "jest.config.js",
            "jest.config.ts",
        ),
        "Vitest": (
            "vitest.config.ts",
            "vitest.config.js",
        ),
        "JUnit": (
            "pom.xml",
            "build.gradle",
        ),
    }

    VIRTUAL_ENVIRONMENTS = (
        ".venv",
        "venv",
        "env",
    )

    def analyze(self, workspace: str | Path) -> RepositoryResult:
        """
        Analyze an existing repository.

        Parameters
        ----------
        workspace:
            Repository root.

        Returns
        -------
        RepositoryResult
        """

        repository = self._validate_repository(workspace)

        language = self._detect_language(repository)
        framework = self._detect_framework(repository)

        project_type = self._detect_project_type(
            repository,
            language,
        )

        build_system = self._detect_build_system(repository)

        dependency_manager = self._detect_dependency_manager(
            repository,
        )

        source_directory = self._detect_source_directory(
            repository,
        )

        entry_point = self._detect_entry_point(repository)

        documentation = self._detect_documentation(
            repository,
        )

        license_file = self._detect_license(repository)

        containerized = self._detect_containerization(
            repository,
        )

        ci_cd = self._detect_ci_cd(repository)

        testing_framework = self._detect_testing_framework(
            repository,
        )

        virtual_environment = (
            self._detect_virtual_environment(
                repository,
            )
        )

        return self._build_result(
            repository=repository,
            language=language,
            framework=framework,
            project_type=project_type,
            build_system=build_system,
            dependency_manager=dependency_manager,
            source_directory=source_directory,
            entry_point=entry_point,
            documentation=documentation,
            license_file=license_file,
            containerized=containerized,
            ci_cd=ci_cd,
            testing_framework=testing_framework,
            virtual_environment=virtual_environment,
        )
        
    
    def _validate_repository(self, workspace: str | Path) -> Path:
        """
        Validate the repository path.
        """

        if not workspace:
            raise ValueError("Workspace path cannot be empty.")

        repository = Path(workspace).expanduser().resolve()

        if not repository.exists():
            raise FileNotFoundError(
                f"Repository does not exist: {repository}"
            )

        if not repository.is_dir():
            raise NotADirectoryError(
                f"{repository} is not a directory."
            )

        return repository

    def _detect_language(self, repository: Path) -> str:
        """
        Detect the primary programming language.
        """

        for language, markers in self.LANGUAGE_MARKERS.items():
            for marker in markers:
                if "*" in marker:
                    if any(repository.rglob(marker)):
                        return language
                elif (repository / marker).exists():
                    return language

        return "Unknown"

    def _detect_framework(self, repository: Path) -> str:
        """
        Detect the primary framework.
        """

        if (repository / "manage.py").exists():
            return "Django"

        if (repository / "artisan").exists():
            return "Laravel"

        if (repository / "next.config.js").exists():
            return "Next.js"

        if (repository / "next.config.ts").exists():
            return "Next.js"

        if (repository / "angular.json").exists():
            return "Angular"

        if (repository / "vue.config.js").exists():
            return "Vue"

        if (repository / "streamlit_app.py").exists():
            return "Streamlit"

        if (repository / "package.json").exists():
            package = (repository / "package.json").read_text(
                encoding="utf-8",
                errors="ignore",
            ).lower()

            if '"react"' in package:
                return "React"

            if '"express"' in package:
                return "Express"

        if (repository / "requirements.txt").exists():
            requirements = (
                repository / "requirements.txt"
            ).read_text(
                encoding="utf-8",
                errors="ignore",
            ).lower()

            if "fastapi" in requirements:
                return "FastAPI"

            if "flask" in requirements:
                return "Flask"

            if "django" in requirements:
                return "Django"

            if "streamlit" in requirements:
                return "Streamlit"

        if (repository / "pyproject.toml").exists():
            pyproject = (
                repository / "pyproject.toml"
            ).read_text(
                encoding="utf-8",
                errors="ignore",
            ).lower()

            if "fastapi" in pyproject:
                return "FastAPI"

            if "flask" in pyproject:
                return "Flask"

            if "django" in pyproject:
                return "Django"

            if "streamlit" in pyproject:
                return "Streamlit"

        return "Unknown"

    def _detect_build_system(self, repository: Path) -> str:
        """
        Detect the project's build system.
        """

        for system, marker in self.BUILD_SYSTEMS.items():
            if (repository / marker).exists():
                return system

        return "Unknown"

    def _detect_dependency_manager(self, repository: Path) -> str:
        """
        Detect the dependency manager.
        """

        if (repository / "poetry.lock").exists():
            return "Poetry"

        if (repository / "Pipfile").exists():
            return "Pipenv"

        if (repository / "requirements.txt").exists():
            return "pip"

        if (repository / "package-lock.json").exists():
            return "npm"

        if (repository / "yarn.lock").exists():
            return "Yarn"

        if (repository / "pnpm-lock.yaml").exists():
            return "pnpm"

        if (repository / "Cargo.toml").exists():
            return "Cargo"

        if (repository / "pom.xml").exists():
            return "Maven"

        if (repository / "build.gradle").exists():
            return "Gradle"

        return "Unknown"

    def _detect_source_directory(
        self,
        repository: Path,
    ) -> str | None:
        """
        Detect the primary source directory.
        """

        for directory in self.SOURCE_DIRECTORIES:
            path = repository / directory

            if path.exists() and path.is_dir():
                return directory

        return None

    def _detect_entry_point(
        self,
        repository: Path,
    ) -> str | None:
        """
        Detect the application's entry point.
        """

        for entry in self.ENTRY_POINTS:
            path = repository / entry

            if path.exists():
                return entry

        return None
    
    
    def _detect_project_type(
        self,
        repository: Path,
        language: str,
    ) -> str:
        """
        Detect the overall project type.
        """

        if language == "Python":
            if (repository / "manage.py").exists():
                return "Web Application"

            if (
                (repository / "app.py").exists()
                or (repository / "main.py").exists()
            ):
                return "API Service"

            if (repository / "notebooks").exists():
                return "Data Science Project"

            if (
                (repository / "train.py").exists()
                or (repository / "models").exists()
            ):
                return "Machine Learning Project"

        if language in ("JavaScript", "TypeScript"):
            if (
                (repository / "next.config.js").exists()
                or (repository / "next.config.ts").exists()
            ):
                return "Web Application"

            if (repository / "package.json").exists():
                return "Web Application"

        if (
            (repository / "README.md").exists()
            and not self._detect_entry_point(repository)
        ):
            return "Library"

        return "Unknown"

    def _detect_documentation(
        self,
        repository: Path,
    ) -> list[str]:
        """
        Detect documentation files.
        """

        documentation: list[str] = []

        for file in self.DOCUMENTATION_FILES:
            if (repository / file).exists():
                documentation.append(file)

        return documentation

    def _detect_license(
        self,
        repository: Path,
    ) -> str | None:
        """
        Detect the repository license.
        """

        for file in self.LICENSE_FILES:
            if (repository / file).exists():
                return file

        return None

    def _detect_containerization(
        self,
        repository: Path,
    ) -> bool:
        """
        Detect Docker support.
        """

        return any(
            (repository / file).exists()
            for file in self.CONTAINER_FILES
        )

    def _detect_ci_cd(
        self,
        repository: Path,
    ) -> bool:
        """
        Detect CI/CD configuration.
        """

        github = repository / ".github" / "workflows"

        if github.exists() and github.is_dir():
            return True

        return any(
            (repository / file).exists()
            for file in self.CI_CD_FILES
        )

    def _detect_testing_framework(
        self,
        repository: Path,
    ) -> str:
        """
        Detect the testing framework.
        """

        for framework, markers in self.TEST_FRAMEWORKS.items():
            for marker in markers:
                if (repository / marker).exists():
                    return framework

        return "Unknown"

    def _detect_virtual_environment(
        self,
        repository: Path,
    ) -> bool:
        """
        Detect a local virtual environment.
        """

        return any(
            (repository / env).exists()
            for env in self.VIRTUAL_ENVIRONMENTS
        )

    def _build_result(
        self,
        *,
        repository: Path,
        language: str,
        framework: str,
        project_type: str,
        build_system: str,
        dependency_manager: str,
        source_directory: str | None,
        entry_point: str | None,
        documentation: list[str],
        license_file: str | None,
        containerized: bool,
        ci_cd: bool,
        testing_framework: str,
        virtual_environment: bool,
    ) -> RepositoryResult:
        """
        Build the RepositoryResult.
        """

        return RepositoryResult(
            repository_path=repository,
            repository_name=repository.name,
            is_git_repository=(repository / ".git").exists(),
            language=language,
            framework=framework,
            project_type=project_type,
            build_system=build_system,
            dependency_manager=dependency_manager,
            source_directory=source_directory,
            entry_point=entry_point,
            documentation=documentation,
            license_file=license_file,
            containerized=containerized,
            ci_cd=ci_cd,
            testing_framework=testing_framework,
            virtual_environment=virtual_environment,
        )
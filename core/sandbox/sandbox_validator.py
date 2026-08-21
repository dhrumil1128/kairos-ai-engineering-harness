"""
File: core/sandbox/sandbox_validator.py

Purpose:
Validate generated projects
before sandbox execution.

Why:

Projects should never be
executed unless minimum
requirements are satisfied.

This prevents execution
failures caused by missing
files and invalid project
structures.

Architecture:

SandboxManager
       ↓
SandboxValidator
       ↓
Validation Result
       ↓
SandboxExecutor

Responsibilities:

- Validate project structure
- Validate required folders
- Validate required files
- Validate KAIROS metadata
- Prevent invalid execution

V1:
- Project validation

V2:
- Dependency validation

V3:
- Runtime validation

V4:
- Security validation

V5:
- Language-specific validation

V6:
- Container validation

V7:
- Autonomous project auditing

Enterprise:

- Security compliance checks
- Policy validation
- Audit validation
- Dependency governance
- Supply chain verification
- Organizational standards
"""

# Path utilities.
from pathlib import Path

# Sandbox configuration.
from core.sandbox.sandbox_config import (
    SandboxConfig
)


class SandboxValidator:
    """
    Validate projects before
    execution.
    """

    def validate(
        self,
        project_path: str
    ) -> bool:
        """
        Validate project.

        Parameters:
            project_path:
                Generated project.

        Returns:
            Validation status.
        """

        print(
            "\n[SANDBOX VALIDATOR]"
        )

        print(
            f"Project={project_path}"
        )

        # Convert to Path object.
        project = Path(
            project_path
        )

        # Project missing.
        if not project.exists():

            print(
                "[VALIDATOR] Project not found"
            )

            return False

        # Validate directories.
        if not self._validate_directories(
            project
        ):

            return False

        # Validate KAIROS files.
        if not self._validate_kairos_files(
            project
        ):

            return False

        # Validate source code.
        if not self._validate_source(
            project
        ):

            return False

        print(
            "[VALIDATOR] Validation Passed"
        )

        return True

    def _validate_directories(
        self,
        project: Path
    ) -> bool:
        """
        Validate required
        directories.
        """

        for directory in (
            SandboxConfig
            .get_required_directories()
        ):

            path = (
                project
                / directory
            )

            if not path.exists():

                print(
                    f"[VALIDATOR] Missing directory: {directory}"
                )

                return False

        return True

    def _validate_kairos_files(
        self,
        project: Path
    ) -> bool:
        """
        Validate .kairos files.
        """

        kairos_dir = (
            project
            / ".kairos"
        )

        # .kairos missing.
        if not kairos_dir.exists():

            print(
                "[VALIDATOR] Missing .kairos directory"
            )

            return False

        # Required metadata files.
        for filename in (
            SandboxConfig
            .get_required_kairos_files()
        ):

            file_path = (
                kairos_dir
                / filename
            )

            if not file_path.exists():

                print(
                    f"[VALIDATOR] Missing {filename}"
                )

                return False

        return True

    def _validate_source(
        self,
        project: Path
    ) -> bool:
        """
        Validate source code.
        """

        # Validate entrypoint.
        entrypoint = (
            project
            / SandboxConfig.PYTHON_ENTRYPOINT
        )

        if not entrypoint.exists():

            print(
                "[VALIDATOR] Missing src/main.py"
            )

            return False

        # Validate test file.
        test_file = (
            project
            / "tests"
            / "test_main.py"
        )

        if not test_file.exists():

            print(
                "[VALIDATOR] Missing tests/test_main.py"
            )

            return False

        # Validate README.
        readme = (
            project
            / "docs"
            / "README.md"
        )

        if not readme.exists():

            print(
                "[VALIDATOR] Missing docs/README.md"
            )

            return False

        return True

    def validate_docs(
        self,
        project_path: str
    ) -> bool:
        """
        Validate documentation.
        """

        project = Path(
            project_path
        )

        docs_dir = (
            project
            / "docs"
        )

        if not docs_dir.exists():

            print(
                "[VALIDATOR] Missing docs folder"
            )

            return False

        return True

    def validate_tests(
        self,
        project_path: str
    ) -> bool:
        """
        Validate tests folder.
        """

        project = Path(
            project_path
        )

        tests_dir = (
            project
            / "tests"
        )

        if not tests_dir.exists():

            print(
                "[VALIDATOR] Missing tests folder"
            )

            return False

        return True

    def validation_report(
        self,
        project_path: str
    ) -> dict:
        """
        Generate validation report.

        Future:
        Used by recursive healing.
        """

        valid = self.validate(
            project_path
        )

        return {
            "valid": valid,
            "project": project_path
        }
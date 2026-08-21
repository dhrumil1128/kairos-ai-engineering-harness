"""
File: core/sandbox/sandbox_config.py

Purpose:
Central sandbox configuration.

Why:

All sandbox settings should
exist in one location.

This prevents hardcoded values
from being scattered across
the sandbox subsystem.

Architecture:

SandboxManager
      ↓
SandboxConfig
      ↓
SandboxValidator
      ↓
SandboxExecutor

Responsibilities:

- Execution timeout
- Workspace location
- Output limits
- Supported runtimes
- Sandbox policies

V1:
- Local execution settings

V2:
- Resource limits

V3:
- Multi-language support

V4:
- Container configuration

V5:
- Distributed execution

V6:
- Cloud execution policies

V7:
- Autonomous execution profiles

Enterprise:

- Security policies
- Resource quotas
- Execution governance
- Compliance controls
- Multi-tenant isolation
- Audit configuration
- Organization policies
"""


class SandboxConfig:
    """
    Central sandbox configuration.
    """

    # -------------------------
    # Workspace Configuration
    # -------------------------

    # Generated project location.
    WORKSPACE_DIR = (
        "workspace/generated_project"
    )

    # KAIROS project metadata.
    KAIROS_DIR = (
        ".kairos"
    )

    # -------------------------
    # Execution Configuration
    # -------------------------

    # Maximum execution time.
    EXECUTION_TIMEOUT = 30

    # Maximum retries.
    MAX_RETRIES = 3

    # Maximum output length.
    MAX_OUTPUT_LENGTH = 10000

    # -------------------------
    # Python Configuration
    # -------------------------

    # Default Python entrypoint.
    PYTHON_ENTRYPOINT = (
        "src/main.py"
    )

    # Default test command.
    PYTEST_COMMAND = (
        "pytest"
    )

    # -------------------------
    # Validation Rules
    # -------------------------

    # Required project folders.
    REQUIRED_DIRECTORIES = [
        "src",
        "tests",
        "docs"
    ]

    # Required KAIROS files.
    REQUIRED_KAIROS_FILES = [
        "architecture.md",
        "roadmap.md",
        "project_context.md",
        "memory.md"
    ]

    # -------------------------
    # Supported Languages
    # -------------------------

    SUPPORTED_LANGUAGES = [
        "python"
    ]

    # -------------------------
    # Security Configuration
    # -------------------------

    # Block shell execution.
    ALLOW_SHELL_COMMANDS = False

    # Allow internet access.
    ALLOW_NETWORK_ACCESS = False

    # Allow file deletion.
    ALLOW_FILE_DELETION = False

    # -------------------------
    # Future Configuration
    # -------------------------

    # Placeholder for enterprise.
    ENTERPRISE_MODE = False

    @classmethod
    def get_workspace(
        cls
    ) -> str:
        """
        Return workspace path.
        """

        return (
            cls.WORKSPACE_DIR
        )

    @classmethod
    def get_timeout(
        cls
    ) -> int:
        """
        Return execution timeout.
        """

        return (
            cls.EXECUTION_TIMEOUT
        )

    @classmethod
    def get_required_directories(
        cls
    ) -> list:
        """
        Return required folders.
        """

        return (
            cls.REQUIRED_DIRECTORIES
        )

    @classmethod
    def get_required_kairos_files(
        cls
    ) -> list:
        """
        Return required
        documentation files.
        """

        return (
            cls.REQUIRED_KAIROS_FILES
        )
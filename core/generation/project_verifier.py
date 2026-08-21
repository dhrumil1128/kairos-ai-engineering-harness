"""
File:
core/generation/project_verifier.py

Purpose:
Verify that a generated
project is complete before
it enters the validation
pipeline.

Why:

The Code Generator can
produce incomplete or
broken projects.

ProjectVerifier performs
a lightweight pre-flight
verification to detect
common generation issues
before validation and
sandbox execution.

Architecture:

Generation Pipeline
        │
        ▼
Project Verifier
        │
        ├── Entry Point
        ├── Project Structure
        ├── Imports
        ├── Requirements
        ├── Empty Files
        │
        ▼
Validation Pipeline

V2:
- Symbol Resolution

V3:
- Circular Dependency Detection

V4:
- Framework Specific Verification

V5:
- Autonomous Project Repair
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import ast
import re
import importlib.util
import sys


from core.logging.kairos_logger import KairosLogger
from core.python.module_discovery import discover_generated_modules

@dataclass(slots=True)
class VerificationIssue:
    """
    Single verification issue.
    """

    category: str
    severity: str
    message: str
    file: str | None = None


@dataclass(slots=True)
class VerificationResult:
    """
    Verification result.
    """

    success: bool = True

    issues: list[VerificationIssue] = field(
        default_factory=list
    )

    def add_issue(
        self,
        category: str,
        severity: str,
        message: str,
        file: str | None = None,
    ) -> None:

        self.success = False

        self.issues.append(
            VerificationIssue(
                category=category,
                severity=severity,
                message=message,
                file=file,
            )
        )

    @property
    def error_count(self) -> int:
        return sum(
            issue.severity == "error"
            for issue in self.issues
        )

    @property
    def warning_count(self) -> int:
        return sum(
            issue.severity == "warning"
            for issue in self.issues
        )


class ProjectVerifier:
    """
    Verify generated projects
    before validation.
    """

    def __init__(self):

        self.logger = KairosLogger(
            "generation"
        )

    # ------------------------------------------------ #

    def verify(
        self,
        project_root: str | Path,
    ) -> VerificationResult:
        """
        Execute all verification checks.
        """

        project_root = Path(project_root)

        result = VerificationResult()

        self.logger.info(
            "Starting project verification..."
        )

        self._check_project_structure(
            project_root,
            result,
        )

        self._check_entrypoint(
            project_root,
            result,
        )

        self._check_empty_files(
            project_root,
            result,
        )

        self._check_python_syntax(
            project_root,
            result,
        )
        
        self._check_requirements(
            project_root,
            result,
        )
        
        self._check_import_resolution(
            project_root,
            result,
        )
        
        
        self._check_expected_files(
            project_root,
            result,
        )

        self.logger.info(
            f"Verification completed. "
            f"Issues: {len(result.issues)}"
        )

        return result
    # ------------------------------------------------ #

    def _check_entrypoint(
        self,
        project_root: Path,
        result: VerificationResult,
    ) -> None:

        candidates = (
            "main.py",
            "app.py",
            "src/main.py",
        )

        if any(
            (project_root / path).exists()
            for path in candidates
        ):
            return

        if self._is_single_file_python_project(
            project_root
        ):
            return

        result.add_issue(
            category="entrypoint",
            severity="error",
            message="No project entry point found.",
        )

    # ------------------------------------------------ #

    def _check_project_structure(
        self,
        project_root: Path,
        result: VerificationResult,
    ) -> None:

        if not project_root.exists():

            result.add_issue(
                category="structure",
                severity="error",
                message="Project directory does not exist.",
            )

    # ------------------------------------------------ #

    def _check_empty_files(
        self,
        project_root: Path,
        result: VerificationResult,
    ) -> None:

        for file in project_root.rglob("*"):

            if not file.is_file():
                continue

            try:

                if file.stat().st_size == 0:

                    result.add_issue(
                        category="empty_file",
                        severity="warning",
                        message="Generated empty file.",
                        file=str(file.relative_to(project_root)),
                    )

            except OSError:
                continue
            
    
    # ------------------------------------------------- #
    def _check_python_syntax(
        self,
        project_root: Path,
        result: VerificationResult,
    ) -> None:
        """
        Verify every generated Python file
        can be parsed successfully.
        """

        for file in project_root.rglob("*.py"):

            try:

                source = file.read_text(
                    encoding="utf-8"
                )

                ast.parse(source)

            except SyntaxError as error:

                result.add_issue(
                    category="syntax",
                    severity="error",
                    message=(
                        f"Python syntax error "
                        f"({error.msg})"
                    ),
                    file=str(
                        file.relative_to(
                            project_root
                        )
                    ),
                )

            except Exception as error:

                result.add_issue(
                    category="syntax",
                    severity="warning",
                    message=str(error),
                    file=str(
                        file.relative_to(
                            project_root
                        )
                    ),
                )
                
    
    # ------------------------------------------------- #
    def _check_requirements(
        self,
        project_root: Path,
        result: VerificationResult,
    ) -> None:
        """
        Verify requirements.txt.
        """

        if self._is_single_file_python_project(
            project_root
        ):
            return

        requirements = project_root / "requirements.txt"

        if not requirements.exists():

            result.add_issue(
                category="requirements",
                severity="warning",
                message="requirements.txt not found.",
            )

            return

        try:

            packages: set[str] = set()

            for line in requirements.read_text(
                encoding="utf-8"
            ).splitlines():

                line = line.strip()

                if not line:
                    continue

                if line.startswith("#"):
                    continue

                package = re.split(
                    r"[<>=!~\[\]\s]",
                    line,
                    maxsplit=1,
                )[0].lower()

                if not package:

                    result.add_issue(
                        category="requirements",
                        severity="warning",
                        message=f"Invalid requirement entry: '{line}'",
                        file="requirements.txt",
                    )

                    continue

                if package in packages:

                    result.add_issue(
                        category="requirements",
                        severity="warning",
                        message=f"Duplicate package '{package}'",
                        file="requirements.txt",
                    )

                packages.add(package)

        except Exception as error:

            result.add_issue(
                category="requirements",
                severity="error",
                message=str(error),
                file="requirements.txt",
            )
    
    # ------------------------------------------------- #
    def _check_import_resolution(
        self,
        project_root: Path,
        result: VerificationResult,
    ) -> None:
        """
        Verify imported modules can be
        resolved.
        """

        generated_modules = discover_generated_modules(
    file.relative_to(project_root).as_posix()
    for file in project_root.rglob("*.py")
)
        #print("\nGenerated Modules:")
        #print(generated_modules)

        stdlib_modules = self._stdlib_modules()

        for file in project_root.rglob("*.py"):

            try:

                tree = ast.parse(
                    file.read_text(
                        encoding="utf-8"
                    )
                )

            except Exception:
                continue

            for module in self._python_imports(tree):

                root = module.split(".")[0]
                #print(f"Import: {module}  ->  Root: {root}")

                if root in generated_modules:
                    continue

                if root in stdlib_modules:
                    continue

                if importlib.util.find_spec(root):
                    continue

                result.add_issue(
                    category="imports",
                    severity="error",
                    message=f"Missing module '{root}'",
                    file=str(
                        file.relative_to(
                            project_root
                        )
                    ),
                )
    
    # -------------------------------------------------- #
    def _python_imports(
        self,
        tree: ast.AST,
    ) -> set[str]:

        imports: set[str] = set()

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for alias in node.names:
                    imports.add(alias.name)

            elif isinstance(node, ast.ImportFrom):

                if node.level:
                    continue

                if node.module:
                    imports.add(node.module)

        return imports
    
    
 
    def _stdlib_modules(
        self,
    ) -> set[str]:

        modules: set[str] = set(
            getattr(
                sys,
                "stdlib_module_names",
                set(),
            )
        )

        return {
            module
            for module in modules
            if importlib.util.find_spec(module)
            is not None
        }
        
    # --------------------------------------------------------- # 
    def _check_expected_files(
        self,
        project_root: Path,
        result: VerificationResult,
    ) -> None:
        """
        Verify that essential project
        files exist.
        """

        if self._is_single_file_python_project(
            project_root
        ):
            return

        required_files = (
            "README.md",
            ".gitignore",
            "requirements.txt",
        )

        for file in required_files:

            if not (project_root / file).exists():

                result.add_issue(
                    category="structure",
                    severity="warning",
                    message=f"Missing required file: {file}",
                    file=file,
                )

        python_entrypoints = (
            "src/main.py",
            "main.py",
            "app.py",
        )

        if not any(
            (project_root / path).exists()
            for path in python_entrypoints
        ):
            result.add_issue(
                category="entrypoint",
                severity="error",
                message="No valid Python entry point found.",
            )

    def _is_single_file_python_project(
        self,
        project_root: Path,
    ) -> bool:
        if not project_root.exists():
            return False

        root_python_files = [
            file
            for file in project_root.glob("*.py")
            if file.is_file()
        ]
        nested_python_files = [
            file
            for file in project_root.rglob("*.py")
            if file.is_file()
            and file.parent != project_root
        ]

        return (
            len(root_python_files) == 1
            and not nested_python_files
        )

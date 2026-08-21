"""
File: core/architecture/builder.py

Purpose:
Pure, deterministic construction of directories/files/requirements
from a FrameworkTemplate + package_name.

No LLM calls, no I/O, no randomness. Given the same
(template, package_name) this will always produce the same
output - this is what makes the Architect's structural decisions
reproducible across runs, which is the entire point of the
refactor.
"""

from core.architecture.templates import FrameworkTemplate
from core.architecture.blueprint import ArchitectureBlueprint

def _build_capabilities(template: FrameworkTemplate) -> dict:
    return {
        "dependency_injection": template.supports_dependency_injection,
        "blueprints": template.supports_blueprints,
    }
    
    
    
def build_blueprint(
    template: FrameworkTemplate,
    package_name: str,
    *,
    project_name: str,
    project_type: str,
    framework: str,
    language: str,
    entry_point: str,
    requirements: list[str],
) -> ArchitectureBlueprint:
    
    """
    Render a template into concrete directories/files for a
    specific package_name.
    """

    directories = list(dict.fromkeys(template.directories(package_name)))
    files = list(dict.fromkeys(template.files(package_name)))

    if requirements and not _has_dependency_manifest(files):
        files.append("requirements.txt")



    # Build file responsibilities using the actual package name.
    file_responsibilities = {}

    for path, responsibility in template.file_responsibilities.items():

        resolved_path = path.replace(
            "{package}.py",
            f"{package_name}.py"
        )

        resolved_path = resolved_path.replace(
            "{package}",
            package_name
        )

        file_responsibilities[resolved_path] = responsibility
    
    
    if template.include_self_named_module:
        filename = template.self_named_module_filename or f"{package_name}.py"
        self_named_module = f"{package_name}/{filename}"
        if self_named_module not in files:
            files.append(self_named_module)

    directories = _add_implied_directories(directories, files)

    return ArchitectureBlueprint(
    project_name=project_name,
    project_type=project_type,
    framework=framework,
    language=language,

    package_name=package_name,

    entry_point=entry_point,
    entry_module=template.entry_module,
    entry_function=template.entry_function,

    directories=directories,
    files=files,
    requirements=requirements,

    framework_template=template.name,

    code_style=template.code_style,

    capabilities=_build_capabilities(template),

    metadata=dict(template.metadata),
    generation_rules=dict(template.generation_rules),
    validation_rules=dict(template.validation_rules),
    coding_conventions=dict(template.coding_conventions),
    import_rules=dict(template.import_rules),
    file_responsibilities=file_responsibilities,
)


def _add_implied_directories(directories: list[str], files: list[str]) -> list[str]:
    """
    Ensure every parent directory implied by a file path is present
    in `directories`, even for templates that use nested subpaths
    (e.g. package/api/routes.py -> package/api). This is a safety
    net for future templates; current templates are flat so this
    is a no-op for them today.
    """

    seen = dict.fromkeys(directories)

    for file_path in files:
        parts = file_path.split("/")[:-1]
        current = ""
        for part in parts:
            current = f"{current}/{part}" if current else part
            if current not in seen:
                seen[current] = None

    return list(seen.keys())


def _has_dependency_manifest(files: list[str]) -> bool:
    manifests = {
        "requirements.txt",
        "pyproject.toml",
        "package.json",
        "composer.json",
        "pom.xml",
        "cargo.toml",
    }

    return any(
        file_path.replace("\\", "/").lower() in manifests
        for file_path in files
    )


def merge_requirements(mandatory: tuple, suggested) -> list[str]:
    """
    Hybrid dependency resolution:
    - Template-mandatory requirements are always present.
    - LLM-suggested extras are appended.
    - Deduplicated case-insensitively, first-seen casing kept.
    - Non-string / empty entries from the LLM are dropped defensively.
    """

    runtime_names = {
        "python",
        "python3",
        "node",
        "nodejs",
        "java",
        "php",
        "ruby",
        "go",
        "golang",
        "rust",
        "typescript",
        "javascript",
    }
    seen = set()
    merged: list[str] = []

    for requirement in list(mandatory or []) + list(suggested or []):
        if not isinstance(requirement, str) or not requirement.strip():
            continue
        key = requirement.strip().lower()
        if key in runtime_names:
            continue
        if key in seen:
            continue
        seen.add(key)
        merged.append(requirement.strip())

    return merged

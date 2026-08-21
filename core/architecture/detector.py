"""
File: core/architecture/detector.py

Purpose:
Resolve a deterministic FrameworkTemplate from the LLM-provided
free-text `framework` / `project_type` strings.

This is the ONLY place where "does this string mean Flask" logic
lives. Templates own their own aliases (see templates.py), so
registering a new framework never requires touching this file.
"""

from core.architecture.templates import GENERIC_TEMPLATE, FrameworkTemplate, all_templates


def _normalize(value: str) -> str:
    """
    Normalize a free-text string for alias matching:
    lowercase, non-alphanumeric characters collapsed to "_".

    e.g. "Flask-RESTX" -> "flask_restx"
    """
    return "".join(
        character.lower() if character.isalnum() else "_"
        for character in str(value or "")
    ).strip("_")


def resolve_template(framework: str, project_type: str, logger=None) -> FrameworkTemplate:
    """
    Resolve a FrameworkTemplate from LLM-provided hints.

    Both `framework` and `project_type` are checked against every
    registered template's aliases, since the LLM is inconsistent
    about which field it populates (e.g. it may put "flask" in
    project_type instead of framework).

    Falls back to GENERIC_TEMPLATE if nothing matches, logging a
    warning so unmatched frameworks stay visible instead of being
    silently absorbed into the generic shape.
    """

    normalized_framework = _normalize(framework)
    normalized_project_type = _normalize(project_type)
    candidates = {normalized_framework, normalized_project_type}
    candidates.discard("")

    for template in all_templates():
        if template is GENERIC_TEMPLATE:
            continue
        for alias in template.aliases:
            if _normalize(alias) in candidates:
                return template

    if logger is not None:
        logger.info(
            "WARNING: No registered framework template matched "
            f"framework={framework!r} project_type={project_type!r}. "
            "Falling back to generic_python template."
        )

    return GENERIC_TEMPLATE

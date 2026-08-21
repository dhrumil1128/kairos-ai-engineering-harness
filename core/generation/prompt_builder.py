from __future__ import annotations

from core.generation.working_environment import WorkingEnvironment
from core.generation.generation_context import GenerationContext


BANNED_PATTERNS = """
FORBIDDEN — any of these makes the file invalid:
- A function/method body that is only `pass`, `...`, or a bare comment.
- Any comment containing: TODO, FIXME, "implement later", "placeholder", "to be implemented".
- `raise NotImplementedError` unless the architecture explicitly marks this class/file as abstract.
- Defining a class, function, or CLI entry point that already appears under "Existing Symbols" below.
""".strip()

GOOD_VS_BAD_EXAMPLE = """
NOT acceptable:

    def add_task(self, title: str) -> None:
        # TODO: implement logic
        pass

Required standard (same shape, fully implemented):

    def add_task(self, title: str) -> None:
        task = Task(id=self._next_id(), title=title, done=False)
        self._tasks.append(task)
        self._save()
""".strip()


class PromptBuilder:

    def build(
        self,
        environment: WorkingEnvironment,
        context: GenerationContext,
        file_role: str,
        formatted_symbol_context: str,
        formatted_relevant_context: str,
    ) -> str:
        architecture = environment.get_blueprint()

        file_path = environment.get_current_file()
        file_responsibility = architecture.file_responsibilities.get(
            file_path,
            "Implement this file according to its role in the architecture."
        )
        user_request = (
            context.user_request
            or architecture.metadata.get("user_request", "")
        )

        sections: list[str] = []

        sections.append(f"""
User Request:
{user_request}

Project: {architecture.project_type} | Framework: {architecture.framework} | Language: {architecture.language}
Package: {architecture.package_name} | Entry point: {architecture.entry_point}

Runtime Requirements:
{chr(10).join(str(requirement) for requirement in architecture.requirements) or "None"}

Directories:
{chr(10).join(str(d) for d in architecture.directories)}

All Project Files (context only — do NOT implement another file's responsibility here):
{chr(10).join(architecture.files)}

Current File: {file_path}
Role: {file_role}
Responsibility of THIS file, and only this file: {file_responsibility}
""".strip())

        if formatted_symbol_context:
            sections.append(f"""
Existing Symbols (already implemented elsewhere in this project — import and reuse these exactly as named, never redefine or rename them):
{formatted_symbol_context}
""".strip())

        if formatted_relevant_context:
            sections.append(formatted_relevant_context.strip())

        if context:
            sections.append(f"Project Context:\n{context}")

        sections.append(f"""
Rules:
- Preserve explicit user-provided code exactly unless the user explicitly requests modifications.
- If the user provided the full source for {file_path}, that source is the specification: copy it byte-for-byte as the file content.
- Do not refactor, optimize, add type hints, change function bodies, replace print() with logging, change return values, or rewrite control flow in user-provided source.
- Only change user-provided source when the user explicitly requested that modification or the provided source is syntactically invalid.
- Implement only the responsibility listed above for this file. If another file already owns some functionality, call it — never duplicate it.
- Every import must resolve to a symbol listed in "Existing Symbols" above, a module in "All Project Files", or a real standard-library/external module. Never invent imports, files, classes, or functions.
- Prefer the Python standard library. Only add an external dependency if the user explicitly requested it or the framework requires it — and if so, add it to requirements.txt.
- If SQLite (or any local storage) is used, initialize it automatically on first run — no manual setup steps.
- Tests must import only symbols listed above, set up their own state, and run with zero manual steps.
- If this file is documentation (README), it must contain non-empty sections: Overview, Architecture, Installation, Usage (with one real, runnable example), Testing.
- If this file is requirements.txt, output exactly the runtime dependency names listed under Runtime Requirements, one per line, with no prose.
- If database initialization is requested or a database module exists, entry points must call the database initialization helper during startup.
- Route/controller files must delegate business operations to service modules when a service file exists.
- Service files must use schema modules when schemas exist and must not redefine schema classes.
- README files must also include non-empty Requirements, Database Initialization, and Project Structure sections.

Architecture Rules:

- The project's entry point (for example, src/main.py or app.py) must only orchestrate execution.
- Business logic must live in dedicated modules or packages.
- Never duplicate business logic that already exists in another generated file.
- If another generated module already provides the required functionality, import and use it instead of reimplementing it.
- Never use wildcard imports (for example, `from module import *`). Use explicit imports whenever possible.
- Package initialization files (such as `__init__.py`) should expose only the intended public API using explicit imports.
- Every generated file must remain consistent with the project architecture, file responsibilities, and previously generated files.
- If this file is an entry point, it should contain minimal logic and delegate work to reusable modules.
- Do not generate code that contradicts the architecture, file responsibilities, or previously generated files.

{BANNED_PATTERNS}

{GOOD_VS_BAD_EXAMPLE}

Before you finish: re-read your own draft. If any function body is empty or stub-like, any comment says TODO/placeholder, or any import references something not listed above — fix it now, before responding.

Output ONLY the raw content of {file_path}. No markdown fences. No explanation before or after the code.
""".strip())

        return "\n\n".join(sections)

    def format_symbol_context(
        self,
        symbol_index: dict,
    ) -> str:

        if not symbol_index:
            return ""

        sections = []

        for file_path, symbols in symbol_index.items():

            sections.append(
                f"{file_path}"
            )

            for key in (
                "classes",
                "functions",
                "variables",
            ):

                values = symbols.get(
                    key,
                    [],
                )

                if values:

                    sections.append(
                        f"{key}: {', '.join(values)}"
                    )

            sections.append("")

        return "\n".join(
            sections
        )

    def format_relevant_context(
        self,
        relevant_files: dict[str, str],
    ) -> str:
        """
        Format previously generated files for prompt context.
        """

        if not relevant_files:
            return ""

        sections = []

        sections.append(
            "Previously Generated Files:\n"
        )

        for file_path, content in relevant_files.items():

            sections.append(
                f"=== {file_path} ==="
            )

            sections.append(content.strip())

            sections.append("")

        return "\n".join(sections)

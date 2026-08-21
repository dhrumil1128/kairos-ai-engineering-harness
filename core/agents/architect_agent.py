"""
File: core/agents/architect_agent.py

Purpose:
Transform task plans into
high-level system architecture.

Why:

Before implementation begins,
KAIROS should understand:

- Components
- Services
- Modules
- Responsibilities

Architecture:

Planner Agent
      ↓
Architect Agent
      ↓
System Design
      ↓
Coder Agent

Design Note (v2 - deterministic structure):

The LLM is used ONLY to classify high-level intent:
    - framework
    - project_type
    - project_name
    - language
    - suggested dependencies

Directory layout, filenames, and module organization are NEVER
LLM output. They come from a deterministic FrameworkTemplate,
selected via core.architecture.detector and rendered via
core.architecture.builder. Same plan -> same framework detection
-> same template -> byte-identical structure, every run.

Adding support for a new framework (FastAPI, Django, React,
Next.js, Express, CLI, Library, ...) requires only registering a
new FrameworkTemplate in core/architecture/templates.py - this
file does not need to change.

Future Versions:

V2:
- LLM-powered architecture design (superseded - see Design Note above)

V3:
- Dependency analysis

V4:
- Security-aware architecture

V5:
- Distributed system planning
"""

import json
import re

# Base agent functionality.
from core.agents.base_agent import BaseAgent

# Provider manager.
from core.providers.provider_manager import ProviderManager

# Provider registry.
from core.providers.provider_registry import ProviderRegistry

# logging
from core.logging.kairos_logger import KairosLogger

# Deterministic structure registry.
from core.architecture.detector import resolve_template
from core.architecture.builder import build_blueprint, merge_requirements

from core.architecture.blueprint import ArchitectureBlueprint

# Entry point is always fixed - kept as a module-level constant since
# it's referenced in more than one place.
DEFAULT_ENTRY_POINT = "src/main.py"


class ArchitectAgent(BaseAgent):
    """
    KAIROS Architect Agent.

    Responsible for converting
    plans into architecture.

    The LLM classifies intent (framework, project type, naming,
    dependency hints). The Architect owns the resulting project
    structure deterministically via a FrameworkTemplate registry.
    """

    def __init__(self):
        """
        Initialize architect agent.
        """
        super().__init__(name="ArchitectAgent")

        # Create provider manager.
        self.provider_manager = ProviderManager(ProviderRegistry())

        self.provider = "ollama"

        # Architect logger.
        self.logger = KairosLogger("architect")

    def create_architecture(self, plan) -> ArchitectureBlueprint:
        """
        Public API / test compatibility alias for architecture generation.
        Accepts a raw dict plan or any object with an execution_context attribute.
        """

        class DummyContext:
            def __init__(self, p):
                if hasattr(p, "task"):
                    self.execution_context = p
                elif isinstance(p, dict):
                    self.execution_context = type(
                        "Plan",
                        (),
                        {
                            "task": p.get("task", ""),
                            "generated_plan": p.get("generated_plan", ""),
                        },
                    )()
                else:
                    self.execution_context = type(
                        "Plan", (), {"task": str(p), "generated_plan": ""}
                    )()

        wrapped = not hasattr(plan, "execution_context")
        context = plan if not wrapped else plan
        if wrapped:
            context = DummyContext(plan)

        result = self.execute(context)

        # Restore the original plan in memory so callers that pass a raw
        # dict receive the same object back from memory.retrieve("latest_plan").
        if wrapped:
            self.memory.store("latest_plan", plan)

        return result

    def execute(
        self,
        agent_context,
    ) -> ArchitectureBlueprint:
        """
        Generate architecture.

        Parameters:
            agent_context:
                Agent or execution context.

        Returns:
            Architecture definition.
        """
        plan = agent_context.execution_context
        self.memory.store("latest_plan", plan)

        prompt = self._build_intent_prompt(plan, agent_context)

        self.logger.debug(f"Prompt:\n{prompt}")
        response = self.provider_manager.execute(
            task_type="architecture", prompt=prompt
        )

        self.logger.info("Architecture generation completed")

        self.logger.debug(f"Raw Response:\n{response}")

        intent = self._parse_intent_response(response)

        architecture_spec = self._build_deterministic_architecture(
            plan=plan,
            intent=intent,
        )

        self.logger.debug(f"Parsed Architecture:\n{architecture_spec}")

        self._validate_architecture(architecture_spec)

        self.logger.success("Architecture generated successfully")
        return architecture_spec

    # ------------------------------------------------------------------
    # LLM intent classification
    # ------------------------------------------------------------------

    def _build_intent_prompt(
        self,
        plan,
        agent_context,
    ) -> str:
        """
        Build a deliberately narrow prompt. The LLM classifies
        intent only - it is never asked for directories, files,
        entry_point, or package_name. Those are owned by the
        deterministic template registry.
        """

        user_request = plan.task if hasattr(plan, "task") else (
            plan.get("task", "") if isinstance(plan, dict) else str(plan)
        )
        intent_request = self._request_without_paths(user_request)
        planner_output = self._request_without_paths(
            plan.generated_plan if hasattr(plan, "generated_plan") else (
                plan.get("generated_plan", "") if isinstance(plan, dict) else ""
            )
        )

        prompt = f"""
    You are a senior software architect.

    Classify the high-level intent of a software project.

    Return ONLY valid JSON.

    Rules:

    1. No markdown.
    2. No explanations.
    3. No comments.
    4. No code fences.
    5. Valid JSON only.
    6. Do NOT invent directory structures, filenames, module
       layouts, or imports. That is not your responsibility.
    7. Filesystem paths are output destinations only. Do NOT infer
       project_name, project_type, features, domain, or behavior
       from a path or folder name.
    8. Preserve the user's explicit task. If the task is simple
       hello world, classify it as hello world only.

    Required Schema:

    {{
        "project_name": "project_name",
        "project_type": "project_type",
        "framework": "framework_if_any",
        "language": "Python",
        "requirements": [
            "dependency1"
        ]
    }}

    User Request With Paths Removed:

    {intent_request}

    Planner Guidance (High-Level Only):

    The planner output is provided only for understanding the
    user's intent and overall execution strategy. Do NOT copy
    directory structures, filenames, package layouts, module
    layouts, imports, or code organization from it - you are not
    designing project structure, only classifying intent.

    Planner Output:

    {planner_output}
    """

        if agent_context:
            prompt += f"""

        Project Context:

        {agent_context}
        """

        return prompt

    def _request_without_paths(self, request: str) -> str:
        """
        Remove local filesystem paths before intent classification.
        Folder names in output paths are storage locations, not
        product names or feature hints.
        """

        without_windows_paths = re.sub(
            r"[A-Za-z]:\\[^\r\n]+",
            "[target directory]",
            str(request or ""),
        )

        return without_windows_paths.strip()

    def _parse_intent_response(self, response) -> dict:
        """
        Parse the LLM's intent-classification response into a dict.
        Provider-layer parsing may already return a Python object.
        Plain text responses keep the original defensive path
        (strip code fences, slice between first "{" and last "}").
        """

        if isinstance(response, dict):
            return response

        if isinstance(response, list):
            raise ValueError(
                "Architecture response must be a JSON object."
            )

        clean_response = response.replace("```json", "").replace("```", "").strip()

        json_start = clean_response.find("{")
        json_end = clean_response.rfind("}")

        if json_start == -1 or json_end == -1:
            raise ValueError("No JSON object found in architecture response.")

        json_content = clean_response[json_start : json_end + 1]

        return json.loads(json_content)

    # ------------------------------------------------------------------
    # Deterministic structure assembly
    # ------------------------------------------------------------------

    def _build_deterministic_architecture(
        self,
        plan: dict,
        intent: dict
    ) -> ArchitectureBlueprint:
        """
        Assemble the final architecture spec. `intent` supplies
        project_name/project_type/framework/language/requirements
        hints; everything structural is deterministic.
        """

        package_name = self._sanitize_package_name(
            intent.get("package_name", intent.get("project_name", "app"))
        )

        template = resolve_template(
            framework=intent.get("framework", ""),
            project_type=intent.get("project_type", ""),
            logger=self.logger,
        )

        requirements = merge_requirements(
            mandatory=template.mandatory_requirements,
            suggested=intent.get("requirements", []),
        )

        blueprint = build_blueprint(
            template=template,
            package_name=package_name,
            project_name=intent.get("project_name", package_name),
            project_type=intent.get("project_type", ""),
            framework=intent.get("framework", ""),
            language=intent.get("language", "Python"),
            entry_point=template.entry_module or DEFAULT_ENTRY_POINT,
            requirements=requirements,
        )

        task_text = plan.task if hasattr(plan, "task") else (
            plan.get("task", "") if isinstance(plan, dict) else str(plan)
        )
        blueprint.metadata["user_request"] = task_text

        self._apply_request_specific_overrides(blueprint, plan)
        return blueprint

    def _apply_request_specific_overrides(
        self,
        blueprint: ArchitectureBlueprint,
        plan,
    ) -> None:
        """
        Rule 1: If the user explicitly specifies files and/or folders,
        override the template-provided structure with exactly what was
        requested.

        Rule 2: If no explicit file/folder constraints exist, keep the
        existing template behaviour unchanged.
        """
        task_text = plan.task if hasattr(plan, "task") else (
            plan.get("task", "") if isinstance(plan, dict) else str(plan)
        )

        # --- Rule 1: explicit user file/folder constraints ---
        explicit_structure = self._extract_explicit_structure(task_text)

        if explicit_structure:
            files, directories, entry_point = explicit_structure
            blueprint.files = files
            blueprint.directories = directories
            if entry_point:
                blueprint.entry_point = entry_point
                blueprint.entry_module = entry_point

            has_tests = any("test" in f.lower() for f in files)
            has_docs = any(
                f.lower().startswith("docs/") or f.lower().endswith(".md")
                for f in files
            )
            blueprint.generation_rules["generate_tests"] = has_tests
            blueprint.generation_rules["generate_docs"] = has_docs
            blueprint.validation_rules["require_tests"] = has_tests
            return

        # --- Rule 2: fall back to existing single_file_python override ---
        if blueprint.framework_template != "single_file_python":
            return

        filename = self._requested_python_filename(task_text)

        if not filename:
            return

        blueprint.entry_point = filename
        blueprint.entry_module = filename
        blueprint.files = [filename]
        blueprint.directories = []

    def _extract_explicit_structure(
        self, task_text: str
    ) -> tuple[list[str], list[str], str | None] | None:
        """
        Detect and extract explicit file and directory constraints from
        the user request.

        Returns (files, directories, entry_point) if explicit constraints
        are present, or None when no explicit structure was requested so
        that the deterministic template system proceeds unchanged.

        Detection strategy
        ------------------
        The method looks for three unambiguous signals:
          1. A bullet-list "Files:" section  (multi-line)
          2. An inline  "Files: x.py, y.md"  header
          3. An explicit "File name: x.py"   header
        A "Folders:" / "Directories:" list is also supported.
        """
        if not task_text:
            return None

        text = str(task_text)
        requested_files: list[str] = []
        requested_dirs: list[str] = []

        # 1. Structured "Files:" / "Files to generate:" multi-line section
        files_section_match = re.search(
            r"(?im)^\s*(?:Files|Files to generate|Requested files|File list)"
            r"\s*:\s*\n((?:[ \t]*[-*•\d.]+[ \t]+[^\r\n]+\r?\n?)+)",
            text,
        )

        if files_section_match:
            lines = files_section_match.group(1).strip().splitlines()
            for line in lines:
                cleaned = re.sub(r"^\s*[-*•\d.]+\s*", "", line).strip()
                cleaned = cleaned.strip("`'\"")
                if cleaned and not cleaned.startswith("#"):
                    requested_files.append(cleaned)

        # Inline "Files: main.py, README.md" on a single line
        if not requested_files:
            inline_files_match = re.search(
                r"(?im)^\s*(?:Files|Files to generate|Requested files)\s*:\s*([^\r\n]+)",
                text,
            )
            if inline_files_match:
                raw_inline = inline_files_match.group(1).strip()
                # Guard: skip if it looks like a requirement sentence
                if not raw_inline.lower().startswith(
                    ("read", "create", "support", "print", "generate")
                ):
                    items = [
                        f.strip("`'\" ")
                        for f in re.split(r"[,;]", raw_inline)
                        if f.strip()
                    ]
                    for item in items:
                        if "." in item or "/" in item or "\\" in item:
                            requested_files.append(item)

        # 2. Explicit "File name: xyz" or "Filename: xyz" header
        if not requested_files:
            file_name_match = re.search(
                r"(?im)^\s*(?:File name|Filename)\s*:\s*"
                r"([A-Za-z0-9_.-]+(?:\.[A-Za-z0-9_.-]+)?)\s*$",
                text,
            )
            if file_name_match:
                requested_files.append(file_name_match.group(1).strip())

        # 3. Structured "Folders:" or "Directories:" section
        dirs_section_match = re.search(
            r"(?im)^\s*(?:Folders|Directories)\s*:\s*\n"
            r"((?:[ \t]*[-*•\d.]+[ \t]+[^\r\n]+\r?\n?)+)",
            text,
        )
        if dirs_section_match:
            lines = dirs_section_match.group(1).strip().splitlines()
            for line in lines:
                cleaned = (
                    re.sub(r"^\s*[-*•\d.]+\s*", "", line)
                    .strip()
                    .strip("`'\"")
                    .rstrip("/\\")
                )
                if cleaned:
                    requested_dirs.append(cleaned)

        # No explicit constraints found → let template system handle this
        if not requested_files and not requested_dirs:
            return None

        unique_files = list(dict.fromkeys(requested_files))

        # Detect "Do NOT create folders" / "no folders" directive
        no_folders_requested = bool(
            re.search(r"(?i)\b(?:do\s+not|no)\s+create\s+folders?\b", text)
            or re.search(r"(?i)\bno\s+folders?\b", text)
        )

        # Derive parent directories from nested file paths
        derived_dirs: list[str] = list(requested_dirs)
        if not no_folders_requested:
            for f in unique_files:
                parts = f.replace("\\", "/").split("/")
                if len(parts) > 1:
                    parent_dir = "/".join(parts[:-1])
                    if parent_dir and parent_dir not in derived_dirs:
                        derived_dirs.append(parent_dir)

        unique_dirs = (
            list(dict.fromkeys(derived_dirs)) if not no_folders_requested else []
        )

        # Pick the first .py file as the entry point
        entry_point: str | None = None
        for f in unique_files:
            if f.endswith(".py"):
                entry_point = f
                break
        if not entry_point and unique_files:
            entry_point = unique_files[0]

        return unique_files, unique_dirs, entry_point

    def _requested_python_filename(
        self,
        request: str,
    ) -> str | None:
        text = str(request or "")
        patterns = [
            r"(?im)^\s*File name:\s*([A-Za-z0-9_.-]+\.py)\s*$",
            r"(?im)^\s*Filename:\s*([A-Za-z0-9_.-]+\.py)\s*$",
            r"(?i)\b(?:file|script)\s+(?:named|called)\s+([A-Za-z0-9_.-]+\.py)\b",
            r"(?i)\b([A-Za-z0-9_.-]+\.py)\b",
        ]

        for pattern in patterns:
            match = re.search(
                pattern,
                text,
            )

            if match:
                return match.group(1)

        return None

    def _sanitize_package_name(self, package_name) -> str:
        """
        Deterministic package name sanitization (unchanged from the
        original implementation): lowercase alnum, non-alnum -> "_",
        leading digit guarded, empty falls back to "app".
        """

        sanitized = (
            "".join(
                character.lower() if character.isalnum() else "_"
                for character in str(package_name)
            )
            .strip("_")
            or "app"
        )

        if sanitized[0].isdigit():
            sanitized = f"app_{sanitized}"

        return sanitized

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _validate_architecture(
        self,
        architecture_spec: ArchitectureBlueprint
    ) -> None:
        """
        Validate required keys and basic types. Structural content
        (directories/files) is deterministic by construction, so
        this focuses on catching malformed LLM intent fields.
        """

        required_keys = [
            "project_name",
            "project_type",
            "framework",
            "language",

            "entry_point",
            "entry_module",
            "entry_function",

            "package_name",

            "directories",
            "files",
            "requirements",

            "code_style",
            "capabilities",

            "framework_template",
        ]

        for key in required_keys:
            if not hasattr(architecture_spec, key):
                raise ValueError(f"Missing architecture key: {key}")

        for list_field in ("directories", "requirements", "files"):
            value = getattr(architecture_spec, list_field)

            if not isinstance(value, list):
                raise ValueError(
                    f"Architecture field '{list_field}' must be a list, "
                    f"got {type(value).__name__}"
                )

        if not isinstance(architecture_spec.capabilities, dict):
            raise ValueError(
                "Architecture field 'capabilities' must be a dictionary."
            )
        if not isinstance(architecture_spec.metadata, dict):
            raise ValueError(
                "Architecture field 'metadata' must be a dictionary."
            )

        if not isinstance(architecture_spec.generation_rules, dict):
            raise ValueError(
                "Architecture field 'generation_rules' must be a dictionary."
            )

        if not isinstance(architecture_spec.validation_rules, dict):
            raise ValueError(
                "Architecture field 'validation_rules' must be a dictionary."
            )

        if not isinstance(architecture_spec.coding_conventions, dict):
            raise ValueError(
                "Architecture field 'coding_conventions' must be a dictionary."
            )

        if not isinstance(architecture_spec.import_rules, dict):
            raise ValueError(
                "Architecture field 'import_rules' must be a dictionary."
            )

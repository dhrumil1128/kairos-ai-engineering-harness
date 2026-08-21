"""
File: core/agents/coder_agent.py

Purpose:
Generate implementation code
from architecture plans.

Why:

The Coder Agent converts
architectural designs into
implementation tasks.

Architecture:

Planner Agent
      ↓
Architect Agent
      ↓
Coder Agent
      ↓
Execution Layer

Future Versions:

V2:
- Real LLM code generation

V3:
- Multi-file generation

V4:
- Self-correction

V5:
- Autonomous implementation
"""



from pathlib import Path
from types import SimpleNamespace
from typing import Any
import ast
import re

# Base agent functionality.
from core.agents.base_agent import BaseAgent

# Provider manager.
from core.providers.provider_manager import ProviderManager

# Provider registry.
from core.providers.provider_registry import ProviderRegistry


from core.logging.kairos_logger import KairosLogger


#from core.architecture.blueprint import ArchitectureBlueprint

from core.generation.working_environment import WorkingEnvironment
from core.generation.context_builder import ContextBuilder


from core.generation.generation_context import GenerationContext


from core.generation.prompt_builder import PromptBuilder
class CoderAgent(BaseAgent):
    """
    KAIROS Coder Agent.

    Responsible for generating
    implementation output.
    """

    def __init__(self):
        """
        Initialize coder agent.
        """

        super().__init__(name="CoderAgent")

        # Create provider manager.
        self.provider_manager = ProviderManager(ProviderRegistry())

        self.provider = "ollama"
        
        # Coder logger.
        self.logger = KairosLogger(
            "coder"
        )
        
        self.context_builder = ContextBuilder()
        
        self.prompt_builder = PromptBuilder()
        
        
    def execute(
        self,
        agent_context,
    ) -> dict:
        """
        Generate implementation plan.

        Parameters:
            architecture:
                Architecture definition.

        Returns:
            Structured implementation.
        """

        architecture = agent_context.architecture
        #execution_context = agent_context.execution_context
        
        # Audit event.
        self.audit_logger.log_event(
            "CODE_GENERATED",
            "Code generation started"
        )

        # Store architecture.
        self.memory.store(
            "latest_agent_context",
            agent_context,
        )
        
        
            
        self.logger.info(
        "Code generation started"
        )

        self.logger.debug(
            f"Architecture:\n{architecture}"
        )

        # Generated files container.
        environment = WorkingEnvironment(architecture)

        generated_files = []

        while environment.has_pending_files():

            file_path = environment.next_file()

            generation_context = self.context_builder.build(
                environment
            )

            self.logger.info(
                f"Generating {file_path}"
            )

            explicit_content = self._explicit_user_code_for_file(
                context=generation_context,
                file_path=file_path,
            )

            if explicit_content is not None:
                self.logger.info(
                    f"Using explicit user-provided content for {file_path}"
                )
                environment.mark_generated(
                    file_path=file_path,
                    content=explicit_content,
                )
                generated_files = [
                    {
                        "path": path,
                        "content": content,
                    }
                    for path, content in environment
                        .get_generated_files()
                        .items()
                ]
                implementation = {
                    "status": "generated",
                    "architecture": architecture.to_dict(),
                    "implementation_spec": {
                        "files": generated_files,
                    },
                }
                continue

            file_prompt = self._build_file_prompt(
            environment=environment,
            context=generation_context,
        )
            
            
            messages = self._build_file_messages(
                file_prompt
            )
            response = ""
            clean_content = ""

            for attempt in range(1, 4):
                self.logger.debug(
                    f"\n[FILE PROMPT]\n{file_prompt}"
                )

                response = self.provider_manager.execute(
                    task_type="coding",
                    prompt=str(messages[-1]["content"])
                )

                clean_content = self._clean_generated_content(
                    response,
                    file_path=file_path,
                )

                self._log_file_request_diagnostics(
                    file_path=file_path,
                    prompt=file_prompt,
                    messages=messages,
                    response=response,
                    attempt=attempt,
                )

                # Reject responses that appear to contain multiple generated files.
                if response:
                    text = str(response)

                    markers = [
                        "Current File:",
                        "Filename:",
                        "### File:",
                        "## File:",
                    ]

                    marker_count = sum(text.count(marker) for marker in markers)

                    if marker_count > 5:
                        self.logger.warning(
                            f"Provider returned multiple files for {file_path}. Retrying..."
                        )
                        clean_content = ""
                        continue

                if clean_content:
                    break

                self.logger.warning(
                    f"Empty provider response for {file_path} on attempt {attempt}"
                )

            if not clean_content:
                self._log_failed_file_request(
                    file_path=file_path,
                    prompt=file_prompt,
                    messages=messages,
                    response=response,
                )
                raise ValueError(
                    f"Generated empty file content: {file_path}"
                )

            self.logger.debug(
                f"\n[FILE CONTENT] {file_path}\n{clean_content}"
            )

            environment.mark_generated(
                file_path=file_path,
                content=clean_content,
            )
            generated_files = [
                {
                    "path": path,
                    "content": content,
                }
                for path, content in environment
                    .get_generated_files()
                    .items()
            ]
            
            
            implementation = {
                "status": "generated",
                "architecture": architecture.to_dict(),
                "implementation_spec": {
                    "files": generated_files,
                },
            }

        self.memory.store(
            "latest_implementation",
            implementation
        )

        self.logger.debug(
            f"Implementation Spec:\n{implementation['implementation_spec']}"
        )

        self.logger.success(
            "Code generation completed"
        )

        return implementation


    def generate_code(
        self,
        architecture,
        context=None,
    ) -> dict:
        """
        Backward-compatible generation entry point.
        """

        agent_context = SimpleNamespace(
            architecture=architecture,
            execution_context=context,
        )

        return self.execute(
            agent_context,
        )

    
    def _build_file_prompt(
        self,
        *,
        environment: WorkingEnvironment,
        context: GenerationContext,
    ) -> str:
        
    
        file_path = environment.get_current_file()

        symbol_index = context.symbol_index
        
        file_role = self._file_role(file_path)

        relevant_files = environment.get_relevant_files()

        formatted_relevant_context = (
            self.prompt_builder.format_relevant_context(
                relevant_files
            )
        )

        formatted_symbol_context = (
            self.prompt_builder.format_symbol_context(
                symbol_index
            )
        )
        
        prompt = self.prompt_builder.build(
            environment=environment,
            context=context,
            file_role=file_role,
            formatted_symbol_context=formatted_symbol_context,
            formatted_relevant_context=formatted_relevant_context,
        )
        
        return prompt

    def _explicit_user_code_for_file(
        self,
        *,
        context: GenerationContext,
        file_path: str,
    ) -> str | None:
        """
        Preserve literal user-supplied source for simple file requests.
        """

        request = str(context.user_request or "")
        if request.strip() and self._request_asks_for_modification(request):
            return None

        metadata_content = self._explicit_file_content_from_metadata(
            context=context,
            file_path=file_path,
        )
        if metadata_content is not None:
            return metadata_content

        if not request.strip():
            return None

        if not self._is_target_file(
            context=context,
            file_path=file_path,
        ):
            return None

        fenced = self._fenced_code_for_file(
            request=request,
            file_path=file_path,
        )
        if fenced is not None:
            return fenced

        inline = self._python_snippet_from_request(request)
        if inline is not None:
            return inline

        return None

    def _explicit_file_content_from_metadata(
        self,
        *,
        context: GenerationContext,
        file_path: str,
    ) -> str | None:
        metadata = getattr(
            context.architecture,
            "metadata",
            {},
        )

        if not isinstance(metadata, dict):
            return None

        for key in (
            "explicit_files",
            "user_provided_files",
            "file_contents",
        ):
            value = metadata.get(key)

            if not isinstance(value, dict):
                continue

            normalized_file_path = self._normalize_path(file_path)

            for candidate_path, candidate_content in value.items():
                if not isinstance(candidate_content, str):
                    continue

                if self._same_path(
                    str(candidate_path),
                    normalized_file_path,
                ):
                    if self._valid_explicit_content(
                        file_path=file_path,
                        content=candidate_content,
                    ):
                        return candidate_content

        return None

    def _request_asks_for_modification(
        self,
        request: str,
    ) -> bool:
        lowered = request.lower()
        modification_terms = (
            "modify",
            "change",
            "update",
            "refactor",
            "rewrite",
            "improve",
            "optimize",
            "fix",
            "repair",
        )
        return any(
            re.search(
                rf"\b{re.escape(term)}\b",
                lowered,
            )
            for term in modification_terms
        )

    def _is_target_file(
        self,
        *,
        context: GenerationContext,
        file_path: str,
    ) -> bool:
        files = list(context.architecture.files)
        if len(files) == 1 and files[0] == file_path:
            return True

        normalized_request = self._normalize_path(context.user_request)
        normalized_file = self._normalize_path(file_path)
        return normalized_file in normalized_request

    def _fenced_code_for_file(
        self,
        *,
        request: str,
        file_path: str,
    ) -> str | None:
        matches = list(
            re.finditer(
                r"```(?:[A-Za-z0-9_.+-]+)?[ \t]*(?:\r?\n)?(.*?)\r?\n?```",
                request,
                flags=re.DOTALL,
            )
        )

        if not matches:
            return None

        selected = None
        normalized_file = self._normalize_path(file_path)

        if len(matches) == 1:
            selected = matches[0].group(1)
        else:
            for match in matches:
                prefix = request[
                    max(0, match.start() - 200):match.start()
                ]

                if normalized_file in self._normalize_path(prefix):
                    selected = match.group(1)
                    break

        if selected is None:
            return None

        if self._valid_explicit_content(
            file_path=file_path,
            content=selected,
        ):
            return selected

        return None

    def _first_fenced_code_block(
        self,
        request: str,
    ) -> str | None:
        match = re.search(
            r"```(?:[A-Za-z0-9_.+-]+)?[ \t]*(?:\r?\n)?(.*?)\r?\n?```",
            request,
            flags=re.DOTALL,
        )

        if match:
            return match.group(1)

        return None

    def _python_snippet_from_request(
        self,
        request: str,
    ) -> str | None:
        lines = request.splitlines()
        start = None

        code_start = re.compile(
            r"^\s*(def |class |async def |from |import |if __name__|print\()"
        )

        for index, line in enumerate(lines):
            if code_start.match(line):
                start = index
                break

        if start is None:
            return None

        candidate = "\n".join(lines[start:])
        snippet = self._longest_valid_python_prefix(candidate)

        if snippet is None:
            return None

        return snippet

    def _longest_valid_python_prefix(
        self,
        text: str,
    ) -> str | None:
        lines = text.splitlines()

        while lines and not lines[0].strip():
            lines = lines[1:]

        while lines:
            candidate = "\n".join(lines)

            if self._valid_python_source(candidate):
                return candidate

            lines = lines[:-1]

        return None

    def _valid_explicit_content(
        self,
        *,
        file_path: str,
        content: str,
    ) -> bool:
        if not str(content).strip():
            return False

        if self._normalize_path(file_path).endswith(".py"):
            return self._valid_python_source(content)

        return True

    def _valid_python_source(
        self,
        content: str,
    ) -> bool:
        try:
            ast.parse(content)
        except SyntaxError:
            return False

        return True
       
    def _file_role(
        self,
        file_path: str,
    ) -> str:
        suffix = Path(file_path).suffix.lower()
        filename = Path(file_path).name.lower()
        parent = Path(file_path).parent.name.lower()

        if filename == "__init__.py":
            return "Python package initialization. Return ONLY valid Python code."

        if suffix == ".py" and parent == "tests":
            return "Python unit test. Return ONLY valid Python code."

        if suffix == ".py":
            return "Python source file. Return ONLY valid Python code."

        if filename == "requirements.txt":
            return "Python requirements file. Return dependency names only."

        if filename == ".gitignore":
            return "Python .gitignore file."

        if suffix == ".md":
            return "Markdown documentation file."

        return "General project file."






    
   

    def _build_file_messages(
        self,
        prompt: str
    ) -> list[dict[str, str]]:
        """
        Build a fresh message payload for one file generation request.
        """

        return [
            {
                "role": "user",
                "content": str(prompt),
            }
        ]

    def _clean_generated_content(
        self,
        response: Any,
        file_path: str | None = None
    ) -> str:
        """
        Lightweight cleanup after ResponseParser.

        Only strips leading/trailing code fences
        and common LLM preamble text.
        Does not do blanket .replace() to avoid
        corrupting code that contains those patterns.
        """

        text = self._provider_response_text(
            response=response,
            file_path=file_path,
        ).strip()

        # Remove common LLM preamble lines.
        preamble_lines = (
            "Here is the generated Python script:",
            "Here is the implementation:",
            "Here is the code:",
        )

        for preamble in preamble_lines:
            if text.startswith(preamble):
                text = text[len(preamble):].strip()

        # Strip leading code fence.
        lines = text.splitlines()

        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]

        # Strip trailing code fence.
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        return "\n".join(lines).strip()

    def _provider_response_text(
        self,
        *,
        response: Any,
        file_path: str | None = None
    ) -> str:
        """
        Convert provider output into file content text.

        StructuredOutputParser may return Python objects when the
        model emits JSON. Plain text remains supported, while dict/list
        responses are only converted when they contain obvious content.
        """

        if response is None:
            return ""

        if isinstance(response, str):
            return response

        if isinstance(response, dict):
            return self._dict_response_text(
                response=response,
                file_path=file_path,
            )

        if isinstance(response, list):
            return self._list_response_text(
                response=response,
                file_path=file_path,
            )

        return str(response)

    def _dict_response_text(
        self,
        *,
        response: dict,
        file_path: str | None = None
    ) -> str:
        """
        Extract text from common structured provider response shapes.
        """

        for key in (
            "content",
            "code",
            "text",
            "response",
            "file_content",
            "generated_content",
        ):
            value = response.get(key)

            if isinstance(value, str):
                return value

            if isinstance(value, list):
                return self._list_response_text(
                    response=value,
                    file_path=file_path,
                )

        files = response.get("files")

        if isinstance(files, list):
            return self._file_list_response_text(
                files=files,
                file_path=file_path,
            )

        return ""

    def _list_response_text(
        self,
        *,
        response: list,
        file_path: str | None = None
    ) -> str:
        """
        Extract text from structured list responses.
        """

        if not response:
            return ""

        if all(isinstance(item, str) for item in response):
            return "\n".join(response)

        return self._file_list_response_text(
            files=response,
            file_path=file_path,
        )

    def _file_list_response_text(
        self,
        *,
        files: list,
        file_path: str | None = None
    ) -> str:
        """
        Extract content from a list of file-like dictionaries.
        """

        file_items = [
            item
            for item in files
            if isinstance(item, dict)
        ]

        if not file_items:
            return ""

        if file_path:
            normalized_file_path = self._normalize_path(
                file_path
            )

            for item in file_items:
                item_path = item.get("path") or item.get("file")

                if (
                    isinstance(item_path, str)
                    and self._same_path(item_path, normalized_file_path)
                ):
                    return self._dict_response_text(
                        response=item,
                        file_path=file_path,
                    )

        if len(file_items) == 1:
            return self._dict_response_text(
                response=file_items[0],
                file_path=file_path,
            )

        return ""

    def _normalize_path(
        self,
        file_path: str
    ) -> str:
        return str(file_path).strip().replace("\\", "/")

    def _same_path(
        self,
        left: str,
        right: str
    ) -> bool:
        normalized_left = self._normalize_path(
            left
        )
        normalized_right = self._normalize_path(
            right
        )

        return (
            normalized_left == normalized_right
            or normalized_left.endswith(f"/{normalized_right}")
            or normalized_right.endswith(f"/{normalized_left}")
        )

    def _log_file_request_diagnostics(
        self,
        *,
        file_path: str,
        prompt: str,
        messages: list[dict[str, str]],
        response: str,
        attempt: int,
    ) -> None:
        """
        Log one file generation request/response boundary.
        """

        response_text = "" if response is None else str(response)
        preview = response_text[:200].replace(
            "\n",
            "\\n"
        )

        self.logger.debug(
            (
                "[FILE GENERATION TRACE] "
                f"file={file_path} | "
                f"attempt={attempt} | "
                f"prompt_length={len(str(prompt))} | "
                f"messages_sent={len(messages)} | "
                f"provider_request_payload_size={self._request_payload_size(messages)} | "
                f"raw_provider_response_length={len(response_text)} | "
                f"raw_provider_response_preview={preview}"
            )
        )

    def _log_failed_file_request(
        self,
        *,
        file_path: str,
        prompt: str,
        messages: list[dict[str, str]],
        response: str,
    ) -> None:
        """
        Log full request state when both attempts return empty content.
        """

        self.logger.error(
            f"File generation failed after retry: {file_path}"
        )
        self.logger.error(
            f"Failed request prompt:\n{prompt}"
        )
        self.logger.error(
            f"Failed request messages:\n{messages}"
        )
        self.logger.error(
            f"Failed raw provider response:\n{response}"
        )

    def _request_payload_size(
        self,
        messages: list[dict[str, str]]
    ) -> int:
        """
        Return byte size of the per-file provider payload.
        """

        return len(
            str(messages).encode(
                "utf-8"
            )
        )
    
    



    def repair_code(
        self,
        repair_plan: dict,
        implementation: dict
    ) -> dict:
        """
        Repair previously generated
        implementation using a
        structured repair plan.

        Used by:
        Recursive Healing System
        """

        self.audit_logger.log_event(
            "CODE_REPAIR_STARTED",
            "Repair workflow started"
        )

        self.logger.info(
            "Code repair started"
        )

        self.memory.store(
            "latest_repair_plan",
            repair_plan
        )

        repaired_files = []

        for file in implementation[
            "implementation_spec"
        ]["files"]:

            self.logger.info(
                f"Repairing {file['path']}"
            )

            repair_context = self._repair_context(
                repair_plan
            )
            prompt = f"""
            Repair the following file.

            Current File:

            {file['path']}

            Error:

            {repair_context}

            Current Content:

            {file['content']}

            Requirements:

            - Fix the root cause.
            - Preserve working code.
            - Do not include repair plans, analysis, retry metadata, agent names, or validation metadata.
            - If this is requirements.txt, return dependency names only.
            - Return ONLY file content.
            """

            response = (
                self.provider_manager.execute(
                    task_type="coding",
                    prompt=prompt
                )
            )

            repaired_content = self._clean_generated_content(
                response,
                file_path=file["path"],
            )

            if not self._valid_repaired_content(
                path=file["path"],
                content=repaired_content,
            ):
                repaired_content = file["content"]

            repaired_files.append(
                {
                    "path":
                        file["path"],

                    "content":
                        repaired_content
                }
            )

        repaired_implementation = {

            "status":
                "repaired",

            "repair_plan":
                repair_plan,

            "implementation_spec": {

                "files":
                    repaired_files
            }
        }

        self.memory.store(
            "latest_repaired_implementation",
            repaired_implementation
        )

        self.logger.success(
            "Code repair completed"
        )

        return repaired_implementation

    def _repair_context(
        self,
        repair_plan: dict
    ) -> str:
        """
        Build a compact repair context without exposing framework metadata.
        """

        text_parts = []

        for key in [
            "error",
            "message",
            "root_cause",
        ]:
            value = repair_plan.get(key)

            if value:
                text_parts.append(str(value))

        analysis = repair_plan.get("analysis", {})

        if isinstance(analysis, dict):
            for key in [
                "error_type",
                "root_cause",
            ]:
                value = analysis.get(key)

                if value:
                    text_parts.append(str(value))

        if not text_parts:
            text_parts.append("Repair the failing generated file.")

        return "\n".join(text_parts)

    def _valid_repaired_content(
        self,
        *,
        path: str,
        content: str
    ) -> bool:
        stripped = str(content).strip()

        if not stripped:
            return False

        lowered = stripped.lower()
        forbidden = [
            "repair_plan",
            "manualinvestigation",
            "manual_investigation",
            "revieweragent",
            "reviewer_agent",
            "validation_steps",
            "retry",
            "repair plan",
            "analysis",
            "reasoning",
        ]

        if any(item in lowered for item in forbidden):
            return False

        if path.replace("\\", "/").endswith("requirements.txt"):
            requirement = re.compile(
                r"^[A-Za-z0-9_.-]+(?:\[[A-Za-z0-9_,.-]+\])?(?:\s*(?:==|>=|<=|~=|!=|>|<)\s*[A-Za-z0-9_.!*+-]+)?$"
            )

            return all(
                not line.strip()
                or line.strip().startswith("#")
                or requirement.match(line.strip())
                for line in stripped.splitlines()
            )

        if path.endswith(".py"):
            try:
                ast.parse(stripped)
            except SyntaxError:
                return False

        return True

    def _log_raw_llm_output(
        self,
        response: Any
    ) -> None:
        """
        Temporarily log the exact raw LLM response for generation debugging.
        """

        text = "" if response is None else str(response)

        header = "===== RAW LLM OUTPUT ====="
        log_path = (
            Path(".kairos")
            / "logs"
            / "raw_llm_output.txt"
        )
        log_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with log_path.open(
            "a",
            encoding="utf-8"
        ) as file:
            file.write(
                f"{header}\n"
            )
            file.write(
                text
            )
            file.write(
                "\n"
            )

    def _log_content_diagnostic(
        self,
        stage: str,
        content
    ) -> None:
        """
        Log generation content diagnostics without mutating content.
        """

        is_none = content is None
        text = "" if content is None else str(content)
        is_empty = text == ""
        preview = text[:200].replace(
            "\n",
            "\\n"
        )

        self.logger.debug(
            (
                "[CONTENT TRACE] "
                f"{stage} | "
                f"length={len(text)} | "
                f"is_none={is_none} | "
                f"is_empty={is_empty} | "
                f"first_200={preview}"
            )
        )

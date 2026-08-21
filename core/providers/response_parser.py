"""
File: core/providers/response_parser.py

Purpose:
Normalize provider responses.

Why:

Different providers return
different response structures.

KAIROS should operate on a
single standardized format.

Future:

V2:
- Provider-specific parsing

V3:
- Tool call parsing

V4:
- Streaming parsing

V5:
- Structured output parsing
"""

from __future__ import annotations

import ast
import re


class ResponseParser:
    """
    Normalize responses.
    """

    def parse(
        self,
        response: dict
    ) -> dict:
        """
        Parse provider response.

        Parameters:
            response:
                Raw provider response.

        Returns:
            Standardized response.
        """

        return {
            "content": response.get(
                "response",
                ""
            ),
            "provider": response.get(
                "provider",
                ""
            ),
            "success": response.get(
                "success",
                False
            ),
        }

    def get_content(
        self,
        response: dict
    ) -> str:
        """
        Extract content.
        """

        return self.parse(
            response
        )["content"]

    def parse_generation_content(
        self,
        response: str,
        prompt: str = ""
    ) -> str:
        """
        Extract the content for the requested file from an LLM response.
        """

        target_file = self._target_file_from_prompt(
            prompt
        )

        # Try to extract the target section from multi-file responses.
        content = self._extract_target_section(
            response,
            target_file
        )

        # Try the first code block.
        code_block = self._extract_first_code_block(
            response
        )

        # If the code block content is valid Python, prefer it directly.
        # This avoids _clean_python's fallback path which can return prose.
        if (
            code_block is not None
            and target_file
            and target_file.endswith(".py")
        ):
            stripped_block = self._strip_code_fences(
                code_block
            ).strip()

            if self._valid_python(stripped_block):
                return stripped_block

        if content is None:
            content = code_block

        if content is None:
            content = response

        return self._clean_content(
            content,
            target_file
        )

    def _target_file_from_prompt(
        self,
        prompt: str
    ) -> str | None:
        match = re.search(
            r"Current File:\s*\n\s*(.+?)\s*(?:\n\s*\n|$)",
            prompt,
            re.IGNORECASE,
        )

        if not match:
            return None

        return self._normalize_path(
            match.group(1)
        )

    def _extract_target_section(
        self,
        response: str,
        target_file: str | None
    ) -> str | None:
        if not target_file:
            return None

        sections = self._file_sections(
            response
        )

        for index, section in enumerate(sections):
            section_path = self._normalize_path(
                section["path"]
            )

            if not self._same_file(
                section_path,
                target_file
            ):
                continue

            end = (
                sections[index + 1]["start"]
                if index + 1 < len(sections)
                else len(response)
            )
            body = response[
                section["body_start"]:end
            ]
            fenced = self._extract_first_code_block(
                body
            )

            return fenced if fenced is not None else body

        return None

    def _file_sections(
        self,
        response: str
    ) -> list[dict[str, int | str]]:
        patterns = [
            r"(?im)^\s*\*\*([^*\n`]+\.[A-Za-z0-9]+)\*\*\s*$",
            r"(?im)^\s*#+\s*([^#\n`]+\.[A-Za-z0-9]+)\s*$",
            r"(?im)(?:file|current file)\s+`([^`]+)`\s*:",
            r"(?im)(?:file|current file)\s+([^:\n]+\.[A-Za-z0-9]+)\s*:",
        ]
        sections = []

        for pattern in patterns:
            for match in re.finditer(
                pattern,
                response,
            ):
                sections.append(
                    {
                        "path": match.group(1).strip(),
                        "start": match.start(),
                        "body_start": match.end(),
                    }
                )

        return sorted(
            sections,
            key=lambda section: int(section["start"]),
        )

    def _extract_first_code_block(
        self,
        response: str
    ) -> str | None:
        match = re.search(
            r"```(?:[\w.+-]+)?\s*(.*?)```",
            response,
            re.DOTALL,
        )

        if not match:
            unterminated = re.search(
                r"```(?:[\w.+-]+)?\s*(.*)",
                response,
                re.DOTALL,
            )

            if unterminated:
                return unterminated.group(1)

            return None

        return match.group(1)

    def _clean_content(
        self,
        content: str,
        target_file: str | None
    ) -> str:
        cleaned = content.strip()

        if not target_file:
            return cleaned

        if target_file.endswith("requirements.txt"):
            return self._clean_requirements(
                cleaned
            )

        if target_file.endswith(".py"):
            return self._clean_python(
                cleaned
            )

        return self._remove_markdown_file_markers(
            cleaned
        ).strip()

    def _clean_python(
        self,
        content: str
    ) -> str:
        cleaned = self._strip_code_fences(
            self._remove_markdown_file_markers(
                content
            )
        )

        if not cleaned.strip():
            return content.strip()

        # If the cleaned content is already valid Python, return immediately.
        if self._valid_python(cleaned.strip()):
            return cleaned.strip()

        lines = cleaned.splitlines()
        start = 0

        for index, line in enumerate(lines):
            stripped = line.strip()

            if not stripped:
                continue

            # Skip markdown/file labels
            if stripped.startswith(("File:", "Current File:", "Filename:", "**", "###")):
                continue

            # Skip non-Python preamble lines
            # (e.g., "Here's the content for...", "Based on the context...")
            if not self._line_is_python(stripped):
                continue

            # First real line of Python
            start = index
            break

        lines = lines[start:]

        # Remove trailing prose (explanatory text after code).
        lines = self._remove_trailing_prose(lines)

        candidate = "\n".join(lines).strip()

        if self._valid_python(candidate):
            return candidate

        # Try longest valid prefix with quality check.
        prefix = self._longest_valid_python_prefix(lines)

        if prefix and self._looks_like_python_code(prefix):
            return prefix

        # Never return empty when input was non-empty.
        return cleaned.strip()

    def _strip_code_fences(
        self,
        content: str
    ) -> str:
        lines = content.strip().splitlines()

        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        return "\n".join(lines).strip()

    def _longest_valid_python_prefix(
        self,
        lines: list[str]
    ) -> str:
        if not lines:
            return ""

        for end in range(len(lines), 0, -1):
            candidate = "\n".join(
                lines[:end]
            ).strip()

            if (
                self._valid_python(candidate)
                and self._looks_like_python_code(candidate)
            ):
                return candidate

        # Fallback: return the full content even if not valid Python.
        # Returning imperfect code is better than returning nothing.
        return "\n".join(lines).strip()

    def _remove_trailing_prose(
        self,
        lines: list[str]
    ) -> list[str]:
        """
        Remove trailing non-Python prose
        (explanatory text after code blocks).
        """

        if not lines:
            return lines

        end = len(lines)

        # Walk backward past empty lines and prose.
        while end > 0:
            stripped = lines[end - 1].strip()

            if not stripped:
                end -= 1
                continue

            if self._line_is_python(stripped):
                break

            end -= 1

        return lines[:end] if end > 0 else lines

    def _line_is_python(
        self,
        line: str
    ) -> bool:
        """
        Check whether a single line looks
        like Python code.
        """

        if not line:
            return False

        # Comments are Python.
        if line.startswith("#"):
            return True

        # Indented code.
        if line[0] in (" ", "\t"):
            return True

        # Decorators.
        if line.startswith("@"):
            return True

        # String literals (docstrings).
        if line.startswith(('"""', "'''", '"', "'")):
            return True

        # Python keywords and patterns.
        python_starts = (
            "import ", "from ", "def ", "class ",
            "if ", "elif ", "else:", "for ",
            "while ", "try:", "except", "finally:",
            "with ", "return ", "yield ", "raise ",
            "pass", "break", "continue",
            "async ", "await ", "self.", "super(",
            "print(", "assert ",
        )

        if line.startswith(python_starts):
            return True

        # Assignments and function calls.
        if "=" in line or "(" in line:
            return True

        return False

    def _looks_like_python_code(
        self,
        content: str
    ) -> bool:
        """
        Verify content is actual Python code,
        not just prose text that ast.parse
        happens to accept.
        """

        if not content.strip():
            return False

        indicators = 0

        for line in content.splitlines():
            stripped = line.strip()

            if not stripped or stripped.startswith("#"):
                continue

            if any(
                stripped.startswith(keyword)
                for keyword in (
                    "import ", "from ", "def ",
                    "class ", "if ", "return ",
                    "for ", "while ", "@",
                    "try:", "except", "with ",
                    "async ", "raise ",
                )
            ):
                indicators += 1

            elif "=" in stripped or "(" in stripped:
                indicators += 1

        return indicators >= 1

    def _valid_python(
        self,
        content: str
    ) -> bool:
        if not content.strip():
            return False

        try:
            ast.parse(
                content
            )
        except SyntaxError:
            return False

        return True

    def _clean_requirements(
        self,
        content: str
    ) -> str:
        requirement = re.compile(
            r"^[A-Za-z0-9_.-]+(?:\[[A-Za-z0-9_,.-]+\])?(?:\s*(?:==|>=|<=|~=|!=|>|<)\s*[A-Za-z0-9_.!*+-]+)?$"
        )
        lines = []

        for line in content.splitlines():
            stripped = line.strip()

            if not stripped or stripped.startswith("#"):
                continue

            if stripped.endswith(":"):
                continue

            if stripped[0].isupper():
                continue

            if stripped in {
                "class",
                "def",
                "return",
                "pass",
                "import",
                "from",
            }:
                continue

            if requirement.match(stripped):
                lines.append(
                    stripped
                )

        return "\n".join(lines)

    def _remove_markdown_file_markers(
        self,
        content: str
    ) -> str:
        return re.sub(
            r"(?im)^\s*\*\*[^*\n]+\*\*\s*$",
            "",
            content,
        )

    def _normalize_path(
        self,
        path: str
    ) -> str:
        return str(path).strip().strip("`").replace("\\", "/")

    def _same_file(
        self,
        section_path: str,
        target_file: str
    ) -> bool:
        return (
            section_path == target_file
            or section_path.endswith(f"/{target_file}")
            or target_file.endswith(f"/{section_path}")
        )

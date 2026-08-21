"""
File: core/agents/reviewer_agent.py

Purpose:
Review generated code and
provide quality feedback.

Why:

Before code reaches testing,
it should be reviewed for:

- Quality
- Maintainability
- Structure

Architecture:

Coder Agent
      ↓
Reviewer Agent
      ↓
Tester Agent

Future Versions:

V2:
- LLM-powered review

V3:
- Architecture compliance

V4:
- Performance analysis

V5:
- Autonomous review loops
"""

import re
from types import SimpleNamespace
from typing import Any

from core.agents.base_agent import BaseAgent

# Provider manager.
from core.providers.provider_manager import ProviderManager

# Provider registry.
from core.providers.provider_registry import ProviderRegistry


from core.logging.kairos_logger import KairosLogger


class ReviewerAgent(BaseAgent):
    """
    KAIROS Reviewer Agent.

    Responsible for reviewing
    generated code.
    """

    def __init__(self):
        """
        Initialize reviewer agent.
        """

        super().__init__(name="ReviewerAgent")

        # Create provider manager.
        self.provider_manager = ProviderManager(ProviderRegistry())

        self.provider = "ollama"

        # Reviewer logger.
        self.logger = KairosLogger("reviewer")

    def execute(
        self,
        agent_context,
    ) -> dict:
        """
        Review generated code.

        Returns a structured
        validation report that can
        be consumed by the
        recursive healing system.
        """
        
        implementation = agent_context.implementation
        self.logger.info(
    "Reviewer agent started"
)
        self.audit_logger.log_event(
            "CODE_REVIEWED",
            "Review completed"
        )

        self.memory.store(
            "latest_agent_context",
            agent_context
        )
        self.memory.store(
            "latest_review_target",
            implementation
        )

        self.logger.info(
            "Code review started"
        )

        prompt = f"""
    Review the following implementation.

    Perform an evidence-based software review of the provided code only.

    CRITICAL REVIEW RULES:
    1. Review ONLY the actual code provided below. Do NOT assume missing files, un-requested features, or imagined requirements.
    2. Do NOT report vague issues like "Code quality could be improved" or "Implementation looks incomplete". Every issue MUST cite exact code evidence.
    3. If an issue is reported, format it with:
       - File: <file path>
       - Evidence: <exact code line or snippet demonstrating the flaw>
       - Severity: <Critical | High | Medium | Low>
       - Recommendation: <specific fix>

    4. Severity Taxonomy:
       - Critical / High: Syntax errors, runtime crashes (e.g. unhandled zero division), broken imports, or failure of explicit core logic.
       - Medium / Low: Minor documentation suggestions, code style, formatting, or optional refactoring recommendations.

    Validate:

    1. Code Quality
    2. Maintainability
    3. Architecture
    4. Security
    5. Error Handling
    6. Best Practices

    Implementation:

    {implementation}

    Return:

    - Issues Found
    - Severity
    - Recommendations
    - Overall Status

    Approval rules:

    - Use "Overall Status: Accepted" when there are no blocking issues.
    - Use "Overall Status: Accepted with Minor Improvements" when only Medium or Low severity recommendations remain (non-blocking).
    - Use "Overall Status: Changes Requested" ONLY for Critical or High severity issues that block production readiness and are supported by code evidence.
    """
    
       

      

        response = (
            self.provider_manager.execute(
                task_type="review",
                prompt=prompt
            )
        )

        approved = self._is_approved_response(
            response
        )

        review = {

            # Healing system flag.
            "validation_type":
                "review",

            # Review completed.
            "status":
                "reviewed",

            # Original input.
            "implementation":
                implementation,

            # LLM review.
            "generated_review":
                response,

            # Future healing.
            "approved":
                approved,

            # Future reviewer score.
            "score":
                None
        }

        self.memory.store(
            "latest_review",
            review
        )

        self.logger.success(
            "Code review completed"
        )

        self.logger.success(
    "Reviewer agent completed"
)
        return review

    def review_code(
        self,
        implementation: dict,
        context: dict | None = None,
    ) -> dict:
        """
        Backward-compatible review entry point.
        """

        agent_context = SimpleNamespace(
            implementation=implementation,
            context=context,
        )

        return self.execute(
            agent_context,
        )

    def _is_approved_response(
        self,
        response,
    ) -> bool:
        """
        Derive review approval from structured or textual reviewer output.
        """

        conclusion = self._review_conclusion(response)
        has_blocking_issue = self._has_blocking_review_issue(response)

        if conclusion in {
            "accepted",
            "accepted with minor improvements",
            "approved",
            "passed",
            "pass",
            "success",
        }:
            return not has_blocking_issue

        if conclusion in {
            "changes requested",
            "failed",
            "fail",
            "rejected",
            "blocked",
            "blocking",
        }:
            return False

        if isinstance(response, dict):
            approved = response.get("approved")

            if isinstance(approved, bool):
                return approved and not has_blocking_issue

        return not has_blocking_issue

    def _review_conclusion(
        self,
        response: Any,
    ) -> str:
        """
        Extract the review's explicit overall conclusion.
        """

        if isinstance(response, dict):
            for key in (
                "overall_status",
                "overall status",
                "status",
                "conclusion",
                "result",
            ):
                value = response.get(key)

                if isinstance(value, str) and value.strip():
                    return self._normalize_review_status(value)

        text = self._review_text(response)
        match = re.search(
            r"(?im)^\s*(?:[-*]\s*)?overall status\s*:\s*(.+?)\s*$",
            text,
        )

        if match:
            return self._normalize_review_status(
                match.group(1)
            )

        return ""

    def _normalize_review_status(
        self,
        status: str,
    ) -> str:
        normalized = re.sub(
            r"\s+",
            " ",
            str(status).strip().lower().replace("_", " "),
        )
        normalized = normalized.strip(".:;")

        if normalized.startswith("accepted with minor"):
            return "accepted with minor improvements"

        if normalized.startswith("accepted"):
            return "accepted"

        if normalized in {"approved", "passed", "pass", "success"}:
            return normalized

        if normalized.startswith("changes requested"):
            return "changes requested"

        if normalized in {"failed", "fail", "rejected", "blocked", "blocking"}:
            return normalized

        return normalized

    def _has_blocking_review_issue(
        self,
        response: Any,
    ) -> bool:
        """
        Return True only for review failures that should trigger repair.
        """

        if self._structured_has_blocking_severity(response):
            return True

        text = self._review_text(response)

        if self._text_has_blocking_severity(text):
            return True

        return self._text_has_blocking_failure_marker(text)

    def _structured_has_blocking_severity(
        self,
        value: Any,
    ) -> bool:
        if isinstance(value, dict):
            severity = value.get("severity") or value.get("priority")

            if isinstance(severity, str) and severity.strip().lower() in {
                "critical",
                "high",
                "major",
            }:
                return True

            return any(
                self._structured_has_blocking_severity(child)
                for child in value.values()
            )

        if isinstance(value, list):
            return any(
                self._structured_has_blocking_severity(item)
                for item in value
            )

        return False

    def _text_has_blocking_severity(
        self,
        text: str,
    ) -> bool:
        return bool(
            re.search(
                r"(?im)^\s*(?:[-*]\s*)?(?:severity|priority)\s*:\s*(critical|high|major)\b",
                text,
            )
        )

    def _text_has_blocking_failure_marker(
        self,
        text: str,
    ) -> bool:
        blocking_patterns = (
            r"overall status\s*:\s*(failed|fail|rejected|changes requested|blocked|blocking)\b",
            r"status\s*:\s*(failed|fail|rejected|changes requested|blocked|blocking)\b",
            r"\bblocking issue\b",
            r"\bsyntaxerror\b",
            r"\btraceback\b",
        )

        for line in text.splitlines():
            lowered = line.strip().lower()

            if not lowered or self._is_non_blocking_statement(lowered):
                continue

            if any(
                re.search(pattern, lowered)
                for pattern in blocking_patterns
            ):
                return True

        return False

    def _is_non_blocking_statement(
        self,
        line: str,
    ) -> bool:
        return bool(
            re.search(
                r"\b(no|none|not|without)\b.*\b(critical|high|major|blocking|must fix|changes requested|syntaxerror|traceback)\b",
                line,
            )
        ) or bool(
            re.search(
                r"\bseverity\s*:\s*(medium|low|minor|info)\b",
                line,
            )
        )

    def _review_text(
        self,
        response: Any,
    ) -> str:
        if response is None:
            return ""

        if isinstance(response, dict):
            parts = []

            for key in (
                "generated_review",
                "review",
                "message",
                "summary",
                "overall_status",
                "status",
                "conclusion",
            ):
                value = response.get(key)

                if isinstance(value, str):
                    parts.append(value)

            if parts:
                return "\n".join(parts)

        return str(response or "")

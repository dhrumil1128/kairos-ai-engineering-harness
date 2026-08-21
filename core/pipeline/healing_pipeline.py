from __future__ import annotations

import copy
import json
import re
import ast
from typing import Any

from core.logging.kairos_logger import KairosLogger
from core.pipeline.path_resolution import resolve_output_path
from core.pipeline.pipeline_context import PipelineContext
from core.pipeline.pipeline_result import PipelineResult


class HealingPipeline:
    """
    First-class healing stage for validation and sandbox failures.
    """

    def __init__(
        self,
        healing,
        coder,
        filesystem,
        validation_pipeline=None,
        sandbox_pipeline=None,
        max_retries: int = 2,
    ) -> None:
        self.healing = healing
        self.coder = coder
        self.filesystem = filesystem
        self.validation_pipeline = validation_pipeline
        self.sandbox_pipeline = sandbox_pipeline
        self.max_retries = max_retries
        self.logger = KairosLogger("healing")

    @property
    def name(self) -> str:
        return "healing"

    def supports(
        self,
        pipeline: str,
    ) -> bool:
        return pipeline == self.name

    def execute(
        self,
        *,
        context: PipelineContext,
        architecture: dict[str, Any],
        implementation: dict[str, Any],
        validation_result: PipelineResult | None = None,
        sandbox_result: PipelineResult | None = None,
        repair_result: PipelineResult | None = None,
    ) -> PipelineResult:
        self.logger.info("Healing Started")
        self.logger.info("Reading Sandbox Report")

        issues = self._detect_issues(
            validation_result=validation_result,
            sandbox_result=sandbox_result,
            repair_result=repair_result,
        )

        if not issues:
            report = self._report(
                status="success",
                detected_issues=[],
                repairs_applied=[],
                remaining_issues=[],
                confidence=1.0,
                modified_files=[],
            )
            self._write_report(context, report)
            self.logger.success("Healing Completed")

            return PipelineResult.success_result(
                pipeline=self.name,
                data={
                    **report,
                    "implementation": implementation,
                },
            )

        affected_files = self._affected_files(
            issues,
            implementation,
        )

        if not affected_files:
            report = self._report(
                status="failed",
                detected_issues=issues,
                repairs_applied=[],
                remaining_issues=issues,
                confidence=0.2,
                modified_files=[],
            )
            self._write_report(context, report)
            self.logger.error("Healing failed: no affected files identified")

            return PipelineResult.failure_result(
                pipeline=self.name,
                data=report,
            )

        updated_implementation = copy.deepcopy(
            implementation
        )
        repairs_applied = []
        modified_files = []
        validation_after = {}
        sandbox_after = None

        for attempt in range(1, self.max_retries + 1):
            self.logger.info("Applying Fixes")
            repaired_files = self._repair_affected_files(
                issues=issues,
                implementation=updated_implementation,
                affected_files=affected_files,
            )

            if not repaired_files:
                break

            for file in repaired_files:
                self.filesystem.execute(
                    "write",
                    resolve_output_path(
                        context.generated_project,
                        file["path"],
                    ),
                    file["content"],
                )
                repairs_applied.append(
                    {
                        "path": file["path"],
                        "action": "repaired_affected_file",
                        "attempt": attempt,
                    }
                )
                modified_files.append(
                    file["path"]
                )

            updated_implementation = self._merge_repaired_files(
                updated_implementation,
                repaired_files,
            )

            self.logger.info("Re-running Validation")
            validation_after = self._rerun_validation(
                context=context,
                architecture=architecture,
                implementation=updated_implementation,
            )

            remaining_issues = self._remaining_issues(validation_after)

            self.logger.info("Re-running Sandbox")
            sandbox_after = self._rerun_sandbox(
                context=context,
                architecture=architecture,
                implementation=updated_implementation,
            )

            if sandbox_after.success and not remaining_issues:
                break

            issues = self._detect_issues(
                validation_result=self._validation_pipeline_result(
                    validation_after
                ),
                sandbox_result=sandbox_after,
                repair_result=None,
            )
            affected_files = self._affected_files(
                issues,
                updated_implementation,
            )

        remaining_issues = self._remaining_issues(validation_after)
        sandbox_success = bool(
            sandbox_after
            and sandbox_after.success
        )
        success = bool(
            not remaining_issues
            and (
                sandbox_success
                or (
                    sandbox_result
                    and sandbox_result.success
                    and sandbox_after is None
                )
            )
        )
        report = self._report(
            status="success" if success else "failed",
            detected_issues=issues,
            repairs_applied=repairs_applied,
            remaining_issues=remaining_issues,
            confidence=0.8 if success else 0.45,
            modified_files=sorted(set(modified_files)),
            validation=validation_after,
            sandbox=sandbox_after.to_dict() if sandbox_after else {},
        )
        self._write_report(context, report)

        if success:
            self.logger.success("Healing Completed")

            return PipelineResult.success_result(
                pipeline=self.name,
                data={
                    **report,
                    "implementation": updated_implementation,
                },
            )

        self.logger.error("Healing failed")

        return PipelineResult.failure_result(
            pipeline=self.name,
            data={
                **report,
                "implementation": updated_implementation,
            },
        )

    def _detect_issues(
        self,
        *,
        validation_result: PipelineResult | None,
        sandbox_result: PipelineResult | None,
        repair_result: PipelineResult | None,
    ) -> list[dict[str, Any]]:
        issues = []

        repair_resolved_validation = bool(
            repair_result
            and repair_result.success
        )

        if (
            validation_result
            and not validation_result.success
            and not repair_resolved_validation
        ):
            issues.extend(
                self._validation_issues(validation_result.data)
            )

        if sandbox_result and not sandbox_result.success:
            issues.extend(
                self._sandbox_issues(sandbox_result.data)
            )

        if repair_result and not repair_result.success:
            issues.append(
                {
                    "type": "repair_failure",
                    "message": str(repair_result.data),
                    "path": None,
                }
            )

        return self._deduplicate_issues(issues)

    def _validation_issues(
        self,
        data: dict[str, Any],
    ) -> list[dict[str, Any]]:
        issues = []
        report = data.get("report", {})

        for section in report.values():
            if not isinstance(section, dict):
                continue

            for error in section.get("errors", []):
                issues.append(
                    self._issue_from_message(str(error))
                )

        for validator in data.get("failed_validators", []):
            issues.append(
                {
                    "type": "configuration_problem",
                    "message": f"Validator failed: {validator}",
                    "path": None,
                }
            )

        return issues

    def _sandbox_issues(
        self,
        data: dict[str, Any],
    ) -> list[dict[str, Any]]:
        messages = []
        logs = data.get("logs", {})
        messages.extend(data.get("errors", []))
        messages.append(str(logs.get("stderr", "")))

        return [
            self._issue_from_message(message)
            for message in messages
            if str(message).strip()
        ]

    def _issue_from_message(
        self,
        message: str,
    ) -> dict[str, Any]:
        lowered = message.lower()

        if "modulenotfounderror" in lowered or "importerror" in lowered:
            issue_type = "missing_dependency"
        elif "syntaxerror" in lowered or "invalid syntax" in lowered:
            issue_type = "syntax_error"
        elif "filenotfounderror" in lowered:
            issue_type = "incorrect_path"
        elif "runtimeerror" in lowered or "traceback" in lowered:
            issue_type = "runtime_exception"
        elif "config" in lowered or "environment" in lowered:
            issue_type = "configuration_problem"
        elif "nameerror" in lowered:
            issue_type = "missing_import"
        else:
            issue_type = "runtime_exception"

        return {
            "type": issue_type,
            "message": message,
            "path": self._extract_path(message),
        }

    def _extract_path(
        self,
        message: str,
    ) -> str | None:
        match = re.search(
            r'File "([^"]+)"',
            message,
        )

        if match:
            return match.group(1)

        match = re.search(
            r"([A-Za-z]:\\[^\s:]+|[\w./\\-]+\.(?:py|js|java|cpp|cc|cxx|json|md|txt))",
            message,
        )

        if match:
            return match.group(1)

        return None

    def _affected_files(
        self,
        issues: list[dict[str, Any]],
        implementation: dict[str, Any],
    ) -> set[str]:
        implementation_files = {
            file.get("path")
            for file in implementation.get("implementation_spec", {}).get("files", [])
            if file.get("path")
        }
        affected = set()

        for issue in issues:
            issue_path = issue.get("path")

            if not issue_path:
                continue

            normalized_issue_path = str(issue_path).replace("\\", "/")

            for file_path in implementation_files:
                normalized_file_path = str(file_path).replace("\\", "/")

                if (
                    normalized_issue_path.endswith(normalized_file_path)
                    or normalized_file_path.endswith(normalized_issue_path)
                ):
                    affected.add(file_path)

        return affected

    def _implementation_for_files(
        self,
        implementation: dict[str, Any],
        affected_files: set[str],
    ) -> dict[str, Any]:
        scoped = copy.deepcopy(implementation)
        scoped["implementation_spec"] = {
            "files": [
                file
                for file in implementation.get("implementation_spec", {}).get("files", [])
                if file.get("path") in affected_files
            ]
        }

        return scoped

    def _repair_affected_files(
        self,
        *,
        issues: list[dict[str, Any]],
        implementation: dict[str, Any],
        affected_files: set[str],
    ) -> list[dict[str, Any]]:
        repaired_files = []

        for file in implementation.get("implementation_spec", {}).get("files", []):
            path = file.get("path")

            if path not in affected_files:
                continue

            issue_context = self._issue_context_for_file(
                path,
                issues,
            )
            repaired_content = self._repair_file_content(
                file=file,
                issue_context=issue_context,
                implementation=implementation,
                affected_files=affected_files,
            )

            if repaired_content is None:
                continue

            repaired_files.append(
                {
                    "path": path,
                    "content": repaired_content,
                }
            )

        return repaired_files

    def _repair_file_content(
        self,
        *,
        file: dict[str, Any],
        issue_context: dict[str, Any],
        implementation: dict[str, Any],
        affected_files: set[str],
    ) -> str | None:
        path = str(
            file.get("path", "")
        )
        current_content = str(
            file.get("content", "")
        )
        prompt = self._repair_prompt(
            path=path,
            current_content=current_content,
            issue_context=issue_context,
            implementation=implementation,
            affected_files=affected_files,
        )
        
        response = self.coder.provider_manager.execute(
            task_type="coding",
            prompt=prompt,
        )
        
        repaired_content = self._clean_repaired_content(
            response
        )

        if not self._is_valid_repair_content(
            path=path,
            content=repaired_content,
        ):
            return None

        return repaired_content

    def _issue_context_for_file(
        self,
        path: str,
        issues: list[dict[str, Any]],
    ) -> dict[str, Any]:
        matching = []
        normalized_path = path.replace("\\", "/")

        for issue in issues:
            issue_path = str(issue.get("path") or "").replace("\\", "/")

            if not issue_path or issue_path.endswith(normalized_path):
                matching.append(issue)

        messages = [
            str(issue.get("message", ""))
            for issue in matching
            if issue.get("message")
        ]

        return {
            "file": path,
            "error_message": "\n".join(messages),
            "stack_trace": self._stack_trace(messages),
            "failing_validator": self._failing_validator(matching),
        }

    def _is_valid_repair_content(
        self,
        *,
        path: str,
        content: str,
    ) -> bool:
        content = content.strip()

        if not content:
            return False

        # Reject markdown / explanations
        if self._looks_like_explanation(content):
            return False

        suffix = path.rsplit(".", 1)[-1].lower() if "." in path else ""

        # requirements.txt
        if path.replace("\\", "/").endswith("requirements.txt"):
            return self._valid_requirements(content)

        # Python files
        if suffix == "py":
            try:
                tree = ast.parse(content)
            except SyntaxError:
                return False

            # Reject repair metadata accidentally written as code
            forbidden_names = {
                "repair_plan",
                "manual_investigation",
                "analysis",
                "review_required",
                "validation_steps",
            }

            for node in ast.walk(tree):
                # Reject repair metadata variables/functions
                if isinstance(node, ast.Name):
                    if node.id in forbidden_names:
                        return False

                if isinstance(node, ast.FunctionDef):
                    if node.name in forbidden_names:
                        return False

            # Preserve expected structure for known files
            normalized = path.replace("\\", "/")

            if normalized.endswith("src/main.py"):
                if "def main(" not in content:
                    return False

            elif normalized.endswith("calculator/calculator.py"):
                # Accept either a class-based or function-based calculator
                if (
                    "class Calculator" not in content
                    and "def add(" not in content
                ):
                    return False

            elif normalized.endswith("__init__.py"):
                # Empty __init__.py is valid
                return True

        # JSON files
        if suffix == "json":
            try:
                json.loads(content)
            except json.JSONDecodeError:
                return False

        return True

    def _repair_prompt(
        self,
        *,
        path: str,
        current_content: str,
        issue_context: dict[str, Any],
        implementation: dict[str, Any],
        affected_files: set[str],
    ) -> str:
        
        project_files = "\n".join(
            f"- {file.get('path')}"
            for file in implementation.get("implementation_spec", {}).get("files", [])
        )

        affected = "\n".join(
            f"- {path}"
            for path in sorted(affected_files)
        )
        return f"""
            Repair exactly one file.
            Project Files:
            {project_files}

            Affected Files:
            {affected}

            Current File:
            {path}

            Error message:
            {issue_context.get("error_message", "")}

            Stack trace:
            {issue_context.get("stack_trace", "")}

            Failing validator:
            {issue_context.get("failing_validator", "")}

            Current file content:
            {current_content}

            Rules:
            - Return the complete replacement content for this file only.
            - Do not include explanations, markdown, analysis, or reasoning.
            - Preserve working code.
            - Do not modify unrelated files.
            - If this is requirements.txt, return dependency names only.
            """.strip()

    def _clean_repaired_content(
        self,
        content: str,
    ) -> str:
        stripped = content.strip()

        fence = re.fullmatch(
            r"```(?:[\w+-]+)?\s*(.*?)```",
            stripped,
            re.DOTALL,
        )

        if fence:
            stripped = fence.group(1).strip()

        return stripped

    def _looks_like_explanation(
        self,
        content: str,
    ) -> bool:
        lowered = content.lower()
        forbidden = [
            "this code",
            "this file",
            "repair plan",
            "the repair",
            "i fixed",
            "here is",
            "explanation",
            "analysis",
            "reasoning",
            "manualinvestigation",
            "revieweragent",
            "validation_steps",
            "retry",
        ]

        return any(
            phrase in lowered
            for phrase in forbidden
        )

    def _valid_requirements(
        self,
        content: str,
    ) -> bool:
        requirement = re.compile(
            r"^[A-Za-z0-9_.-]+(?:\[[A-Za-z0-9_,.-]+\])?(?:\s*(?:==|>=|<=|~=|!=|>|<)\s*[A-Za-z0-9_.!*+-]+)?$"
        )

        for line in content.splitlines():
            stripped = line.strip()

            if not stripped or stripped.startswith("#"):
                continue

            if not requirement.match(stripped):
                return False

        return True

    def _merge_repaired_files(
        self,
        implementation: dict[str, Any],
        repaired_files: list[dict[str, Any]],
    ) -> dict[str, Any]:
        merged = copy.deepcopy(implementation)
        repaired_by_path = {
            file["path"]: file
            for file in repaired_files
        }
        files = []

        for file in implementation.get("implementation_spec", {}).get("files", []):
            files.append(
                repaired_by_path.get(file.get("path"), file)
            )

        merged["implementation_spec"] = {
            "files": files,
        }

        return merged

    def _stack_trace(
        self,
        messages: list[str],
    ) -> str:
        traces = [
            message
            for message in messages
            if "Traceback" in message
        ]

        return "\n".join(traces)

    def _failing_validator(
        self,
        issues: list[dict[str, Any]],
    ) -> str:
        validators = []

        for issue in issues:
            message = str(
                issue.get("message", "")
            )

            if message.startswith("Validator failed:"):
                validators.append(
                    message.removeprefix("Validator failed:").strip()
                )

        return ", ".join(validators)

    def _rerun_validation(
        self,
        *,
        context: PipelineContext,
        architecture: dict[str, Any],
        implementation: dict[str, Any],
    ) -> dict[str, Any]:
        if self.validation_pipeline is None:
            return {
                "passed": True,
                "summary": {
                    "skipped": True,
                },
            }

        return self.validation_pipeline.execute(
            project_path=context.generated_project,
            architecture=architecture,
            implementation=implementation,
        )

    def _rerun_sandbox(
        self,
        *,
        context: PipelineContext,
        architecture: dict[str, Any],
        implementation: dict[str, Any],
    ) -> PipelineResult:
        if self.sandbox_pipeline is None:
            return PipelineResult.success_result(
                pipeline="sandbox",
                data={
                    "success": True,
                    "status": "skipped",
                    "summary": {
                        "skipped": True,
                    },
                },
            )

        return self.sandbox_pipeline.execute(
            context=context,
            architecture=architecture,
            implementation=implementation,
        )

    def _validation_pipeline_result(
        self,
        validation: dict[str, Any],
    ) -> PipelineResult:
        if validation.get("passed", False):
            return PipelineResult.success_result(
                pipeline="validation",
                data=validation,
            )

        return PipelineResult.failure_result(
            pipeline="validation",
            data=validation,
        )

    def _remaining_issues(
        self,
        validation_after: dict[str, Any],
    ) -> list[dict[str, Any]]:
        if validation_after.get("passed", False):
            return []

        return self._validation_issues(validation_after)

    def _report(
        self,
        *,
        status: str,
        detected_issues: list[dict[str, Any]],
        repairs_applied: list[dict[str, Any]],
        remaining_issues: list[dict[str, Any]],
        confidence: float,
        modified_files: list[str],
        validation: dict[str, Any] | None = None,
        sandbox: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return {
            "status": status,
            "detected_issues": detected_issues,
            "repairs_applied": repairs_applied,
            "remaining_issues": remaining_issues,
            "confidence": confidence,
            "modified_files": modified_files,
            "validation": validation or {},
            "sandbox": sandbox or {},
        }

    def _write_report(
        self,
        context: PipelineContext,
        report: dict[str, Any],
    ) -> None:
        self.filesystem.execute(
            "write",
            resolve_output_path(
                context.generated_project,
                ".kairos",
                "healing.json",
            ),
            json.dumps(report, indent=2),
        )

    def _deduplicate_issues(
        self,
        issues: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        seen = set()
        unique = []

        for issue in issues:
            key = (
                issue.get("type"),
                issue.get("message"),
                issue.get("path"),
            )

            if key in seen:
                continue

            seen.add(key)
            unique.append(issue)

        return unique

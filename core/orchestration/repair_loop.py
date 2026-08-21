from __future__ import annotations

import re
from typing import Any

from core.logging.kairos_logger import KairosLogger


class RepairLoop:
    """
    Runs bounded code repair when review fails.
    """

    def __init__(
        self,
        *,
        coordinator,
        config,
        logger: KairosLogger | None = None,
    ) -> None:
        self._coordinator = coordinator
        self._config = config
        self._logger = logger or KairosLogger("orchestration")

    def run(
        self,
        *,
        agent_context,
        implementation: dict[str, Any],
        review: dict[str, Any],
    ) -> dict[str, Any]:
        max_retries = max(
            0,
            int(getattr(self._config, "max_retries", 0)),
        )

        if max_retries == 0:
            return self._failure(
                agent_context=agent_context,
                implementation=implementation,
                review=review,
                message="Review failed and repair retries are disabled.",
                attempts=0,
            )

        current_context = agent_context
        current_implementation = implementation
        current_review = review

        for attempt in range(1, max_retries + 1):
            self._logger.info(
                f"Repair attempt {attempt} of {max_retries}"
            )

            repair_plan = self._build_repair_plan(
                review=current_review,
                attempt=attempt,
            )

            affected = self._affected_files(
                review=current_review,
                implementation=current_implementation,
            )

            if affected:
                target_implementation = self._scope_implementation(
                    current_implementation,
                    affected,
                )
            else:
                target_implementation = current_implementation

            repaired = self._coordinator.repair(
                agent_context=current_context,
                repair_plan=repair_plan,
                implementation=target_implementation,
            )

            if affected:
                merged_implementation = self._merge_repaired_files(
                    current_implementation,
                    repaired.get("implementation", {}),
                )
            else:
                merged_implementation = repaired.get("implementation", current_implementation)

            current_implementation = merged_implementation
            current_review = repaired["review"]
            if hasattr(repaired.get("agent_context"), "with_updates"):
                current_context = repaired["agent_context"].with_updates(
                    implementation=current_implementation,
                )
            else:
                current_context = repaired.get("agent_context", current_context)

            if repaired["success"]:
                self._logger.success(
                    "Repair review passed"
                )
                return {
                    "success": True,
                    "message": repaired["message"],
                    "implementation": current_implementation,
                    "review": current_review,
                    "agent_context": current_context,
                    "attempts": attempt,
                }

        return self._failure(
            agent_context=current_context,
            implementation=current_implementation,
            review=current_review,
            message="Review failed after maximum repair attempts.",
            attempts=max_retries,
        )

    def _affected_files(
        self,
        review: dict[str, Any],
        implementation: dict[str, Any],
    ) -> set[str]:
        review_text = str(
            review.get("generated_review")
            or review.get("message")
            or review
        )

        files = (
            implementation.get("implementation_spec", {})
            .get("files", [])
        )
        if not isinstance(files, list):
            return set()

        known_paths = [
            f.get("path") for f in files
            if isinstance(f, dict) and f.get("path")
        ]

        affected = set()
        review_text_normalized = review_text.replace("\\", "/")

        for file_path in known_paths:
            norm_path = file_path.replace("\\", "/")
            base_name = norm_path.split("/")[-1]

            if norm_path.lower() in review_text_normalized.lower():
                affected.add(file_path)
                continue

            pattern = r'(?<![\w.-])' + re.escape(base_name) + r'(?![\w.-])'
            if re.search(pattern, review_text_normalized, re.IGNORECASE):
                affected.add(file_path)

        return affected

    def _scope_implementation(
        self,
        implementation: dict[str, Any],
        affected: set[str],
    ) -> dict[str, Any]:
        scoped = dict(implementation)
        spec = dict(implementation.get("implementation_spec", {}))
        files = spec.get("files", [])

        scoped["implementation_spec"] = {
            **spec,
            "files": [
                file for file in files
                if isinstance(file, dict) and file.get("path") in affected
            ],
        }
        return scoped

    def _merge_repaired_files(
        self,
        implementation: dict[str, Any],
        repaired: dict[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(repaired, dict):
            return implementation

        repaired_files = (
            repaired.get("implementation_spec", {})
            .get("files", [])
        )
        if not isinstance(repaired_files, list):
            return implementation

        repaired_by_path = {
            file["path"]: file
            for file in repaired_files
            if isinstance(file, dict) and file.get("path")
        }

        merged = dict(implementation)
        spec = dict(implementation.get("implementation_spec", {}))
        orig_files = spec.get("files", [])

        merged_files = []
        for file in orig_files:
            if isinstance(file, dict) and file.get("path") in repaired_by_path:
                merged_files.append(repaired_by_path[file["path"]])
            else:
                merged_files.append(file)

        orig_paths = {f.get("path") for f in orig_files if isinstance(f, dict)}
        for path, file in repaired_by_path.items():
            if path not in orig_paths:
                merged_files.append(file)

        merged["implementation_spec"] = {
            **spec,
            "files": merged_files,
        }
        return merged

    def _build_repair_plan(
        self,
        *,
        review: dict[str, Any],
        attempt: int,
    ) -> dict[str, Any]:
        review_text = str(
            review.get("generated_review")
            or review.get("message")
            or review
        )

        return {
            "error": "ReviewerAgent reported failure.",
            "message": review_text,
            "root_cause": "Generated implementation did not satisfy review criteria.",
            "attempt": attempt,
            "review": review,
        }

    def _failure(
        self,
        *,
        agent_context,
        implementation: dict[str, Any],
        review: dict[str, Any],
        message: str,
        attempts: int,
    ) -> dict[str, Any]:
        self._logger.error(
            message
        )

        return {
            "success": False,
            "message": message,
            "implementation": implementation,
            "review": review,
            "agent_context": agent_context,
            "attempts": attempts,
        }


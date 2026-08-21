from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any


@dataclass(frozen=True)
class AgentContext:
    task: str
    normalized_task: str
    task_type: str
    complexity: str
    workspace: object
    repository: object
    repository_summary: dict[str, Any]
    project_summary: dict[str, Any]
    execution_summary: dict[str, Any]
    available_tools: tuple[str, ...]
    constraints: dict[str, Any]
    execution_steps: tuple[str, ...]
    execution_context: object
    architecture: Any = None
    implementation: dict[str, Any] | None = None
    review: dict[str, Any] | None = None

    def with_updates(self, **updates: Any) -> "AgentContext":
        return replace(self, **updates)

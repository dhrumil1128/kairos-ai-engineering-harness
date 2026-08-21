from dataclasses import dataclass
from typing import Any


@dataclass
class ExecutionContext:
    task: str
    normalized_task: str
    task_type: str
    complexity: str
    workspace: object
    repository: object
    config: object
    requires_code_generation: bool
    requires_repository_context: bool
    requires_validation: bool
    execution_steps: tuple[str, ...]
    generated_plan: str = ""
    metadata: dict[str, Any] | None = None

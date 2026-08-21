from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExecutionResult:
    success: bool
    message: str = ""
    task: str | None = None
    task_type: str | None = None
    complexity: str | None = None
    repository: object | None = None
    output: Any = None
    artifacts: list[Any] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": "completed" if self.success else "failed",
            "success": self.success,
            "message": self.message,
            "task": self.task,
            "task_type": self.task_type,
            "complexity": self.complexity,
            "output": self.output,
            "artifacts": self.artifacts,
            "metadata": self.metadata,
            "data": self.data,
        }

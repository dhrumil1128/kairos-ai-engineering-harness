from dataclasses import dataclass


@dataclass
class TaskContext:
    prompt: str
    goal: str | None = None
    task_type: str | None = None
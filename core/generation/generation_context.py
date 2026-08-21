from __future__ import annotations

from dataclasses import dataclass

from core.architecture.blueprint import ArchitectureBlueprint
from core.generation.project_index import ProjectIndex


@dataclass(slots=True)
class GenerationContext:
    architecture: ArchitectureBlueprint
    user_request: str
    current_file: str | None
    generated_files: dict[str, str]
    pending_files: list[str]
    generation_history: list[str]
    symbol_index: dict[str, dict]
    project_memory: dict
    project_index: ProjectIndex

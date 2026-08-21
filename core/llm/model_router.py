"""
File: core/llm/model_router.py

Purpose:
Select the most appropriate model
for a given task.

Why:

Not every task requires the most
expensive model.

The Model Router helps optimize:

- Cost
- Speed
- Accuracy

Architecture:

Task
    ↓
Model Router
    ↓
Provider Manager
    ↓
Selected Model

Future Versions:

V2:
- Cost-aware routing

V3:
- Token-aware routing

V4:
- Performance analytics

V5:
- Dynamic model benchmarking
"""

# Structured typing.
from typing import Dict


class ModelRouter:
    """
    Selects models based on task type.
    """

    def __init__(self):
        """
        Initialize routing rules.
        """

        self.routes: Dict[
            str,
            str
        ] = {
            "summary": "gemini-flash",
            "coding": "gpt-5",
            "architecture": "claude-opus",
            "embedding": "ollama-embed",
        }

    def get_model(
        self,
        task_type: str
    ) -> str:
        """
        Return model for task type.
        """

        return self.routes.get(
            task_type,
            "gpt-5"
        )

    def add_route(
        self,
        task_type: str,
        model: str
    ) -> None:
        """
        Add routing rule.
        """

        self.routes[
            task_type
        ] = model

    def count(self) -> int:
        """
        Return total routes.
        """

        return len(self.routes)
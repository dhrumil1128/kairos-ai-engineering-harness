"""
File: core/agents/task_graph.py

Purpose:
Manage task dependencies and
execution order.

Why:

Complex workflows require tasks
to depend on one another.

Architecture:

Planner Agent
        ↓
Task Graph
        ↓
Execution Engine

Future:

Parallel Execution
Dependency Resolution
Workflow Optimization
"""

from typing import Dict
from typing import List


class TaskGraph:
    """
    Manage task relationships.
    """

    def __init__(self):
        """
        Initialize graph.
        """

        self.tasks: Dict[
            str,
            List[str]
        ] = {}

    def add_task(
        self,
        task_name: str,
        dependencies: List[str] | None = None
    ) -> None:
        """
        Add task and dependencies.
        """

        self.tasks[
            task_name
        ] = dependencies or []

    def get_dependencies(
        self,
        task_name: str
    ) -> List[str]:
        """
        Return task dependencies.
        """

        return self.tasks.get(
            task_name,
            []
        )

    def exists(
        self,
        task_name: str
    ) -> bool:
        """
        Check task existence.
        """

        return task_name in self.tasks

    def count(self) -> int:
        """
        Return task count.
        """

        return len(self.tasks)
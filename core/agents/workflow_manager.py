"""
File: core/agents/workflow_manager.py

Purpose:
Manage workflow execution plans.

Why:

A workflow consists of multiple
tasks that must be tracked and
executed in a structured manner.

Architecture:

Planner Agent
        ↓
Task Graph
        ↓
Workflow Manager
        ↓
Execution Engine

Future Versions:

V2:
- Dependency resolution

V3:
- Parallel workflows

V4:
- Workflow recovery

V5:
- Distributed workflows
"""

# Structured typing.
from typing import List


class WorkflowManager:
    """
    Manage workflow plans.
    """

    def __init__(self):
        """
        Initialize workflow manager.
        """

        self.tasks: List[str] = []

    def add_task(
        self,
        task: str
    ) -> None:
        """
        Add workflow task.
        """

        self.tasks.append(
            task
        )

    def get_tasks(
        self
    ) -> List[str]:
        """
        Return workflow tasks.
        """

        return self.tasks

    def count(
        self
    ) -> int:
        """
        Return workflow task count.
        """

        return len(
            self.tasks
        )

    def clear(
        self
    ) -> None:
        """
        Clear workflow.
        """

        self.tasks.clear()
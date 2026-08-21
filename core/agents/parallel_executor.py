"""
File: core/agents/parallel_executor.py

Purpose:
Execute multiple agent tasks
in parallel.

Why:

Sequential execution becomes slow
as the number of agents grows.

Example:

Bad:

Planner
 ↓
Architect
 ↓
Security
 ↓
Research

Good:

Architect ─┐
Security  ─┼─ Parallel
Research  ─┘

Architecture:

Agent Orchestrator
        ↓
Parallel Executor
        ↓
Multiple Agents

Future Versions:

V2:
- Async execution

V3:
- Thread pool execution

V4:
- Process pool execution

V5:
- Distributed execution
"""

# Structured typing.
from typing import Callable
from typing import Any


class ParallelExecutor:
    """
    Basic parallel execution layer.

    Version 1:

    Simulates execution of multiple
    tasks and collects results.

    Future:

    Real concurrent execution.
    """

    def execute(
        self,
        tasks: list[Callable]
    ) -> list[Any]:
        """
        Execute task list.

        Parameters:
            tasks:
                Callable functions.

        Returns:
            Results from all tasks.
        """

        results = []

        for task in tasks:

            results.append(
                task()
            )

        return results
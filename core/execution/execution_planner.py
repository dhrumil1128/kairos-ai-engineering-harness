"""
Execution Planner Module.

The ExecutionPlanner is responsible for transforming a user task
and repository understanding into a structured execution plan.

Responsibilities
----------------
- Analyze the requested task
- Understand repository capabilities
- Decide execution strategy
- Estimate execution complexity
- Determine required execution stages
- Produce an immutable execution context

This module NEVER:

- Executes tools
- Calls an LLM
- Reads or writes project files
- Modifies repository state
- Executes shell commands
"""

from __future__ import annotations

#from pathlib import Path

from .execution_context import ExecutionContext
from .execution_engine_config import ExecutionEngineConfig
from .repository_result import RepositoryResult
from .workspace_result import WorkspaceResult


class ExecutionPlanner:
    """
    Plans how KAIROS should solve a task.

    This component converts repository understanding into
    a deterministic execution strategy without performing
    any execution.
    """

    IMPLEMENTATION_TASKS = (
        "implement",
        "create",
        "build",
        "develop",
        "generate",
        "write",
        "add",
    )

    MODIFICATION_TASKS = (
        "modify",
        "change",
        "update",
        "refactor",
        "rewrite",
        "improve",
        "optimize",
        "replace",
    )

    ANALYSIS_TASKS = (
        "analyze",
        "inspect",
        "review",
        "explain",
        "understand",
        "summarize",
    )

    DEBUG_TASKS = (
        "debug",
        "fix",
        "repair",
        "resolve",
        "investigate",
    )

    TEST_TASKS = (
        "test",
        "verify",
        "validate",
        "check",
    )

    DOCUMENTATION_TASKS = (
        "document",
        "describe",
        "comment",
    )

    def plan(
        self,
        *,
        task: str,
        workspace: WorkspaceResult,
        repository: RepositoryResult,
        config: ExecutionEngineConfig,
    ) -> ExecutionContext:
        """
        Create an execution plan.

        Parameters
        ----------
        task:
            User request.

        workspace:
            Workspace discovery result.

        repository:
            Repository understanding result.

        config:
            Engine configuration.

        Returns
        -------
        ExecutionContext
        """

        normalized_task = self._normalize_task(task)

        task_type = self._detect_task_type(
            normalized_task,
        )

        complexity = self._estimate_complexity(
            normalized_task,
        )

        requires_code_generation = (
            self._requires_code_generation(
                task_type,
            )
        )

        requires_repository_context = (
            self._requires_repository_context(
                task_type,
            )
        )

        requires_validation = (
            self._requires_validation(
                task_type,
            )
        )

        execution_steps = self._build_execution_steps(
            task_type,
        )

        return self._build_context(
            task=task,
            normalized_task=normalized_task,
            task_type=task_type,
            complexity=complexity,
            workspace=workspace,
            repository=repository,
            config=config,
            requires_code_generation=requires_code_generation,
            requires_repository_context=requires_repository_context,
            requires_validation=requires_validation,
            execution_steps=execution_steps,
        )
        
    
    def _normalize_task(self, task: str) -> str:
        """
        Normalize the user task for planning.
        """

        if not task:
            raise ValueError("Task cannot be empty.")

        return " ".join(task.strip().lower().split())

    def _detect_task_type(
        self,
        task: str,
    ) -> str:
        """
        Determine the primary task type.
        """

        for keyword in self.IMPLEMENTATION_TASKS:
            if keyword in task:
                return "implementation"

        for keyword in self.MODIFICATION_TASKS:
            if keyword in task:
                return "modification"

        for keyword in self.DEBUG_TASKS:
            if keyword in task:
                return "debugging"

        for keyword in self.TEST_TASKS:
            if keyword in task:
                return "testing"

        for keyword in self.DOCUMENTATION_TASKS:
            if keyword in task:
                return "documentation"

        for keyword in self.ANALYSIS_TASKS:
            if keyword in task:
                return "analysis"

        return "general"

    def _estimate_complexity(
        self,
        task: str,
    ) -> str:
        """
        Estimate task complexity.
        """

        word_count = len(task.split())

        if word_count <= 5:
            return "low"

        if word_count <= 20:
            return "medium"

        return "high"

    def _requires_code_generation(
        self,
        task_type: str,
    ) -> bool:
        """
        Determine whether code generation is required.
        """

        return task_type in {
            "implementation",
            "modification",
            "debugging",
        }

    def _requires_repository_context(
        self,
        task_type: str,
    ) -> bool:
        """
        Determine whether repository understanding is required.
        """

        return task_type in {
            "implementation",
            "modification",
            "debugging",
            "testing",
            "analysis",
        }

    def _requires_validation(
        self,
        task_type: str,
    ) -> bool:
        """
        Determine whether output validation is required.
        """

        return task_type in {
            "implementation",
            "modification",
            "debugging",
            "testing",
        }

    def _build_execution_steps(
        self,
        task_type: str,
    ) -> list[str]:
        """
        Build the ordered execution pipeline.
        """

        steps = [
            "prepare_context",
        ]

        if task_type in {
            "implementation",
            "modification",
            "debugging",
            "analysis",
        }:
            steps.append("analyze_repository")

        if task_type == "analysis":
            steps.append("analyze_request")

        if task_type == "documentation":
            steps.append("collect_information")
            steps.append("generate_documentation")

        if task_type == "testing":
            steps.extend(
                [
                    "locate_tests",
                    "validate_changes",
                ]
            )

        if task_type in {
            "implementation",
            "modification",
            "debugging",
        }:
            steps.extend(
                [
                    "plan_changes",
                    "generate_solution",
                    "validate_solution",
                ]
            )

        steps.append("finalize")

        return steps
    
    
    
    def _build_context(
        self,
        *,
        task: str,
        normalized_task: str,
        task_type: str,
        complexity: str,
        workspace: WorkspaceResult,
        repository: RepositoryResult,
        config: ExecutionEngineConfig,
        requires_code_generation: bool,
        requires_repository_context: bool,
        requires_validation: bool,
        execution_steps: list[str],
    ) -> ExecutionContext:
        """
        Build the immutable execution context.

        Parameters
        ----------
        task:
            Original user task.

        normalized_task:
            Normalized task.

        task_type:
            Detected task type.

        complexity:
            Estimated execution complexity.

        workspace:
            Workspace discovery result.

        repository:
            Repository understanding result.

        config:
            Engine configuration.

        requires_code_generation:
            Whether code generation is required.

        requires_repository_context:
            Whether repository analysis is required.

        requires_validation:
            Whether solution validation is required.

        execution_steps:
            Ordered execution pipeline.

        Returns
        -------
        ExecutionContext
        """

        return ExecutionContext(
            task=task,
            normalized_task=normalized_task,
            task_type=task_type,
            complexity=complexity,
            workspace=workspace,
            repository=repository,
            config=config,
            requires_code_generation=requires_code_generation,
            requires_repository_context=requires_repository_context,
            requires_validation=requires_validation,
            execution_steps=tuple(execution_steps),
            generated_plan=self._format_generated_plan(
                execution_steps
            ),
            metadata={
                "requires_code_generation":
                    requires_code_generation,
                "requires_repository_context":
                    requires_repository_context,
                "requires_validation":
                    requires_validation,
            },
        )

    def _format_generated_plan(
        self,
        execution_steps: list[str],
    ) -> str:
        """
        Build the textual plan consumed by downstream agents.
        """

        return "\n".join(
            f"{index}. {step}"
            for index, step in enumerate(
                execution_steps,
                start=1,
            )
        )

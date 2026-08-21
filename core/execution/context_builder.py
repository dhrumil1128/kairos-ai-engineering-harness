"""
Context Builder Module.

Builds the complete execution context consumed by KAIROS agents.

Responsibilities
----------------
- Gather execution information
- Gather workspace information
- Gather repository information
- Gather engine configuration
- Gather available tools
- Produce a unified AgentContext

This module NEVER:

- Calls an LLM
- Executes tools
- Modifies files
- Performs planning
- Executes code
"""

from __future__ import annotations

from .agent_context import AgentContext
from .execution_context import ExecutionContext
from .execution_engine_config import ExecutionEngineConfig


class ContextBuilder:
    """
    Builds the complete context supplied to every agent.
    """

    def build(
        self,
        *,
        execution_context: ExecutionContext,
        config: ExecutionEngineConfig,
    ) -> AgentContext:
        """
        Build the complete agent context.
        """

        repository_summary = (
            self._build_repository_summary(
                execution_context,
            )
        )

        project_summary = (
            self._build_project_summary(
                execution_context,
            )
        )

        available_tools = (
            self._collect_available_tools(
                config,
            )
        )

        execution_summary = (
            self._build_execution_summary(
                execution_context,
            )
        )

        constraints = (
            self._build_constraints(
                config,
            )
        )

        return self._build_agent_context(
            execution_context=execution_context,
            repository_summary=repository_summary,
            project_summary=project_summary,
            execution_summary=execution_summary,
            available_tools=available_tools,
            constraints=constraints,
        )
        
    def _build_repository_summary(
        self,
        execution_context: ExecutionContext,
    ) -> dict:
        """
        Build a concise repository summary.
        """

        repository = execution_context.repository

        return {
            "name": repository.repository_name,
            "path": str(repository.repository_path),
            "language": repository.language,
            "framework": repository.framework,
            "project_type": repository.project_type,
            "build_system": repository.build_system,
            "dependency_manager": repository.dependency_manager,
            "source_directory": repository.source_directory,
            "entry_point": repository.entry_point,
            "is_git_repository": repository.is_git_repository,
        }

    def _build_project_summary(
        self,
        execution_context: ExecutionContext,
    ) -> dict:
        """
        Build a project summary.
        """

        repository = execution_context.repository

        return {
            "documentation": repository.documentation,
            "license": repository.license_file,
            "containerized": repository.containerized,
            "ci_cd": repository.ci_cd,
            "testing_framework": repository.testing_framework,
            "virtual_environment": repository.virtual_environment,
        }

    def _collect_available_tools(
        self,
        config: ExecutionEngineConfig,
    ) -> list[str]:
        """
        Collect all enabled tools.
        """

        tools: list[str] = []

        if config.enable_file_tools:
            tools.append("FileSystem")

        if config.enable_terminal:
            tools.append("Terminal")

        if config.enable_web_search:
            tools.append("WebSearch")

        if config.enable_memory:
            tools.append("Memory")

        if config.enable_mcp:
            tools.append("MCP")

        return tools

    def _build_execution_summary(
        self,
        execution_context: ExecutionContext,
    ) -> dict:
        """
        Build execution metadata.
        """

        return {
            "task": execution_context.task,
            "task_type": execution_context.task_type,
            "complexity": execution_context.complexity,
            "execution_steps": list(
                execution_context.execution_steps
            ),
            "requires_code_generation":
                execution_context.requires_code_generation,
            "requires_repository_context":
                execution_context.requires_repository_context,
            "requires_validation":
                execution_context.requires_validation,
        }

    def _build_constraints(
        self,
        config: ExecutionEngineConfig,
    ) -> dict:
        """
        Build execution constraints.
        """

        return {
            "max_iterations": config.max_iterations,
            "max_file_changes": config.max_file_changes,
            "allow_terminal": config.enable_terminal,
            "allow_web_search": config.enable_web_search,
            "allow_memory": config.enable_memory,
            "allow_mcp": config.enable_mcp,
        }
        
    
    def _build_agent_context(
        self,
        *,
        execution_context: ExecutionContext,
        repository_summary: dict,
        project_summary: dict,
        execution_summary: dict,
        available_tools: list[str],
        constraints: dict,
    ) -> AgentContext:
        """
        Build the complete AgentContext.

        Parameters
        ----------
        execution_context:
            Execution planning result.

        repository_summary:
            Repository metadata.

        project_summary:
            Project metadata.

        execution_summary:
            Execution information.

        available_tools:
            Tools available to the agent.

        constraints:
            Engine execution constraints.

        Returns
        -------
        AgentContext
        """

        return AgentContext(
            task=execution_context.task,
            normalized_task=execution_context.normalized_task,
            task_type=execution_context.task_type,
            complexity=execution_context.complexity,

            workspace=execution_context.workspace,
            repository=execution_context.repository,

            repository_summary=repository_summary,
            project_summary=project_summary,
            execution_summary=execution_summary,

            available_tools=tuple(available_tools),
            constraints=constraints,

            execution_steps=execution_context.execution_steps,
            execution_context=execution_context,
        )

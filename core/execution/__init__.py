from .workspace_discovery import WorkspaceDiscovery
from .repository_understanding import RepositoryUnderstanding
from .execution_planner import ExecutionPlanner
from .execution_context import ExecutionContext
from .execution_result import ExecutionResult

__all__ = [
    "AutonomousExecutionEngine",
    "WorkspaceDiscovery",
    "RepositoryUnderstanding",
    "ExecutionPlanner",
    "ExecutionContext",
    "ExecutionResult",
]


def __getattr__(name: str):
    if name == "AutonomousExecutionEngine":
        from .autonomous_execution_engine import AutonomousExecutionEngine

        return AutonomousExecutionEngine

    raise AttributeError(name)

from __future__ import annotations

import time
from typing import Any

from core.logging.kairos_logger import KairosLogger
from core.router.intent_handler import IntentHandler
from core.router.route_executor import RouteExecutor
from core.router.workflow_planner import WorkflowPlanner


class AutomationEngine:
    """Owns desktop, browser, and filesystem automation execution."""

    AUTOMATION_ROUTES = {"desktop", "browser", "filesystem"}

    def __init__(
        self,
        *,
        workflow_planner: WorkflowPlanner,
        intent_handler: IntentHandler,
        route_executor: RouteExecutor,
        logger: KairosLogger | None = None,
    ) -> None:
        self.workflow_planner = workflow_planner
        self.intent_handler = intent_handler
        self.route_executor = route_executor
        self.logger = logger or KairosLogger("automation")

    def execute(self, command: str, route: str | None = None) -> dict[str, Any]:

            # First validate the route
            if route not in self.AUTOMATION_ROUTES:
                return self._failure(f"Unsupported automation route: {route}")

            # Only automation routes may use workflows
            workflow_result = self._execute_workflow(command)

            if workflow_result is not None:
                return workflow_result

            intent = self.intent_handler.parse(command, route)

            if not self.intent_handler.is_supported(intent):
                return self._failure("Unsupported automation intent.")

            return self._normalize_result(self.route_executor.execute(intent))

    def _execute_workflow(self, command: str) -> dict[str, Any] | None:
        if not self.workflow_planner.has_workflow(command):
            return None

        workflow = self.workflow_planner.create_workflow(command)
        #print("DEBUG WORKFLOW:", workflow)
        workflow = self._validate_workflow(workflow)
        #print("DEBUG VALIDATED:", workflow)

        if not workflow:
            return None

        results = []

        for step in workflow:
            results.append(self._normalize_result(self.route_executor.execute(step)))
            self._wait_after(step)

        #print("DEBUG RETURNING WORKFLOW")
        return {
            "status": "success",
            "message": "Workflow completed",
            "workflow": results,
        }

    def _validate_workflow(self, workflow: Any) -> list[dict[str, Any]]:
        if not isinstance(workflow, list):
            return []

        return [
            step
            for step in workflow
            if isinstance(step, dict)
            and isinstance(step.get("action"), str)
            and "target" in step
        ]

    def _wait_after(self, step: dict[str, Any]) -> None:
        wait_after = step.get("wait_after", 0)

        if not wait_after:
            return

        try:
            seconds = int(wait_after)
        except (TypeError, ValueError):
            return

        if seconds > 0:
            time.sleep(seconds)

    def _normalize_result(self, result: Any) -> dict[str, Any]:
        if isinstance(result, dict):
            return result

        return {
            "status": "success",
            "message": result,
        }

    def _failure(self, message: str) -> dict[str, Any]:
        self.logger.info(message)

        return {
            "status": "failed",
            "message": message,
        }

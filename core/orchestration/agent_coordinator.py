from __future__ import annotations

from typing import Any

from core.logging.kairos_logger import KairosLogger


class AgentCoordinator:
    """
    Coordinates agent execution order and context handoff.
    """

    def __init__(
        self,
        *,
        architect,
        coder,
        reviewer,
        logger: KairosLogger | None = None,
    ) -> None:
        self._architect = architect
        self._coder = coder
        self._reviewer = reviewer
        self._logger = logger or KairosLogger("orchestration")

    def run_architect(self, agent_context):
        return self._run_agent(
            agent_name="ArchitectAgent",
            agent=self._architect,
            agent_context=agent_context,
        )

    def run_coder(self, agent_context):
        return self._run_agent(
            agent_name="CoderAgent",
            agent=self._coder,
            agent_context=agent_context,
        )

    def run_reviewer(self, agent_context):
        return self._run_agent(
            agent_name="ReviewerAgent",
            agent=self._reviewer,
            agent_context=agent_context,
        )

    def run_lifecycle(self, agent_context) -> dict[str, Any]:
        architecture = self.run_architect(agent_context)
        architect_context = agent_context.with_updates(
            architecture=architecture,
        )

        implementation = self.run_coder(architect_context)
        coder_context = architect_context.with_updates(
            implementation=implementation,
        )

        review = self.run_reviewer(coder_context)
        reviewer_context = coder_context.with_updates(
            review=review,
        )

        return {
            "success": self.review_passed(review),
            "message": self._review_message(review),
            "architecture": architecture,
            "implementation": implementation,
            "review": review,
            "agent_context": reviewer_context,
        }

    def repair(
        self,
        *,
        agent_context,
        repair_plan: dict[str, Any],
        implementation: dict[str, Any],
    ) -> dict[str, Any]:
        repaired_implementation = self._coder.repair_code(
            repair_plan,
            implementation,
        )

        repaired_context = agent_context.with_updates(
            implementation=repaired_implementation,
        )

        review = self.run_reviewer(repaired_context)

        return {
            "success": self.review_passed(review),
            "message": self._review_message(review),
            "implementation": repaired_implementation,
            "review": review,
            "agent_context": repaired_context.with_updates(
                review=review,
            ),
        }

    def review_passed(self, review: Any) -> bool:
        if not isinstance(review, dict):
            return False

        approved = review.get("approved")

        if isinstance(approved, bool):
            return approved

        status = str(review.get("status", "")).lower()
        return status in {"approved", "passed", "success"}

    def _review_message(self, review: Any) -> str:
        if not isinstance(review, dict):
            return "Reviewer returned an invalid review result."

        for key in ("message", "summary", "generated_review"):
            value = review.get(key)

            if value:
                return str(value)

        return "Review completed."

    def _run_agent(
        self,
        *,
        agent_name: str,
        agent,
        agent_context,
    ):
        self._logger.info(
            f"{agent_name} started"
        )

        try:
            result = agent.execute(
                agent_context,
            )
        except Exception as exc:
            self._logger.error(
                f"{agent_name} failed: {exc}"
            )
            raise

        self._logger.success(
            f"{agent_name} completed"
        )

        return result

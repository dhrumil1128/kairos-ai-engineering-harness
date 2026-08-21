"""
File: core/agents/planner_agent.py

Purpose:
Create structured execution plans.

Why:

Every task should first be
understood and decomposed.

Architecture:

User
   ↓
Planner Agent
   ↓
Execution Plan
   ↓
Architect Agent

Future Versions:

V2:
- LLM Planning

V3:
- Multi-Step Planning

V4:
- Dependency Analysis

V5:
- Autonomous Planning
"""

# Base functionality.
from core.agents.base_agent import BaseAgent

# Provider imports.
from core.providers.provider_manager import ProviderManager

from core.providers.provider_registry import ProviderRegistry


from core.logging.kairos_logger import KairosLogger


class PlannerAgent(BaseAgent):
    """
    KAIROS Planner Agent.
    """

    def __init__(self):
        """
        Initialize planner.
        """

        super().__init__(name="PlannerAgent")

        # Create provider manager.
        self.provider_manager = ProviderManager(ProviderRegistry())

        self.provider = "ollama"

        # Planner logger.
        self.logger = KairosLogger("planner")

    def create_plan(self, task: str, context: dict | None = None) -> dict:
        """
        Create structured plan.
        """

        # Generate planning prompt.
        prompt = f"""
Create a structured execution plan for the user's requested software task.

User Request:
{task}

Rules:
- Treat any filesystem path as the output destination only.
- Do not infer project purpose, project name, features, or domain from folder names in paths.
- Preserve the user's explicit task exactly. For example, if the user asks for hello world, plan only hello world.
- Do not expand a simple task into an unrelated larger app.
"""
        
        # ----------------------------------
        # Context Injection
        # ----------------------------------

        if context:

            prompt += f"""

        Project Context:

        {context}
        """

        self.logger.info("Planning started")

        self.logger.debug(f"Prompt:\n{prompt}")

        # Execute provider.
        response = self.provider_manager.execute(
            task_type="planning",
            prompt=prompt,
        )

        self.logger.debug(f"Raw Response:\n{response}")

        # Build plan.
        plan = {
            "task": task,
            "status": "planned",
            "next_agent": ("ArchitectAgent"),
            "generated_plan": response,
        }

        self.logger.debug(f"Generated Plan:\n{plan}")
        # Store in memory.
        self.memory.store("latest_plan", plan)

        # Audit event.
        self.audit_logger.log_event("PLAN_CREATED", task)

        self.logger.success("Planning completed")
        return plan

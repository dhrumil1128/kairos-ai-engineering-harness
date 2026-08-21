"""
File: core/agents/tester_agent.py

Purpose:
Validate generated code and
report testing results.

Why:

Before deployment, code should
be tested to verify correctness.

Architecture:

Coder Agent
      ↓
Reviewer Agent
      ↓
Security Agent
      ↓
Tester Agent

Future Versions:

V2:
- Unit test generation

V3:
- Integration testing

V4:
- Regression testing

V5:
- Autonomous test execution
"""

from core.agents.base_agent import (
    BaseAgent
)

# Provider manager.
from core.providers.provider_manager import (
    ProviderManager
)

# Provider registry.
from core.providers.provider_registry import (
    ProviderRegistry
)


from core.logging.kairos_logger import KairosLogger

class TesterAgent(BaseAgent):
    """
    KAIROS Tester Agent.

    Responsible for validating
    implementation output.
    """

    def __init__(self):
        """
        Initialize tester agent.
        """

        super().__init__(
            name="TesterAgent"
        )
        
        
        # Create provider manager.
        self.provider_manager = (
            ProviderManager(
                ProviderRegistry()
            )
        )
        
        self.provider = (
        "ollama"
        )


        # Tester logger.
        self.logger = KairosLogger(
            "tester"
        )

    def run_tests(
        self,
        review: dict,
        context: dict | None = None
    ) -> dict:
        """
        Execute validation workflow.

        Returns a structured
        testing report that can
        be consumed by the
        recursive healing system.
        """

        self.audit_logger.log_event(
            "TEST_EXECUTED",
            "Testing completed"
        )

        self.memory.store(
            "latest_test_target",
            review
        )

        self.logger.info(
            "Testing started"
        )

        prompt = f"""
    Validate the reviewed implementation.

    Perform professional testing.

    Validate:

    1. Functional Correctness
    2. Edge Cases
    3. Error Handling
    4. Integration Risks
    5. Regression Risks
    6. Production Readiness

    Review:

    {review}

    Return:

    - Test Findings
    - Risks
    - Failed Areas
    - Recommendations
    - Overall Status
    """
    
            # ----------------------------------
        # Context Injection
        # ----------------------------------

        if context:

            prompt += f"""

Project Context:

{context}
"""

        response = (
            self.provider_manager.execute(
                task_type="testing",
                prompt=prompt
            )
        )

        test_result = {

            # Healing system flag.
            "validation_type":
                "testing",

            # Testing completed.
            "status":
                "tested",

            # Review input.
            "review":
                review,

            # LLM test report.
            "generated_test_report":
                response,

            # Future healing.
            "passed":
                True,

            # Future tester score.
            "score":
                None
        }

        self.memory.store(
            "latest_test_result",
            test_result
        )

        self.logger.success(
            "Testing completed"
        )

        return test_result
"""
File: core/healing/execution_loop.py

Purpose:
Coordinate execution,
error analysis,
repair planning,
validation,
and retry workflows.

Why:

A production-grade autonomous
system should not stop after
identifying an error.

Instead:

Failure
   ↓
Analyze
   ↓
Repair Plan
   ↓
Review
   ↓
Test
   ↓
Validate
   ↓
Retry

Architecture:

Execution
   ↓
Error
   ↓
Error Analyzer
   ↓
Self Correction
   ↓
Validation Pipeline
   ↓
Retry Manager
   ↓
Retry

Future Versions:

V2:
- ReviewerAgent integration

V3:
- TesterAgent integration

V4:
- Automatic code patching

V5:
- Fully autonomous repair loop
"""

from core.healing.error_analyzer import (
    ErrorAnalyzer
)

from core.healing.retry_manager import (
    RetryManager
)

from core.healing.self_correction import (
    SelfCorrection
)


class ExecutionLoop:
    """
    Coordinate self-healing
    execution workflows.
    """

    def __init__(self):
        """
        Initialize components.
        """

        # Analyze failures.
        self.error_analyzer = (
            ErrorAnalyzer()
        )

        # Retry controller.
        self.retry_manager = (
            RetryManager()
        )

        # Repair planner.
        self.self_correction = (
            SelfCorrection()
        )

    def process_error(
        self,
        error_message: str,
        attempt: int
    ) -> dict:
        """
        Process execution failure
        and generate recovery
        workflow.
        """

        # Verify retry allowed.
        if not self.retry_manager.should_retry(
            attempt
        ):
            return {
                "status": (
                    "failed"
                ),
                "reason": (
                    "Retry limit reached"
                )
            }

        # Analyze failure.
        analysis = (
            self.error_analyzer.analyze(
                error_message
            )
        )

        # Build repair workflow.
        repair_plan = (
            self.self_correction.generate_fix(
                analysis
            )
        )

        # Extract validation pipeline.
        validation_steps = (
            repair_plan.get(
                "validation_steps",
                []
            )
        )

        return {

            # Recovery required.
            "status":
                "retry",

            # Error analysis.
            "analysis":
                analysis,

            # Generated repair workflow.
            "repair_plan":
                repair_plan,

            # Future reviewer pipeline.
            "review_required":
                True,

            # Future tester pipeline.
            "test_required":
                True,

            # Validation checklist.
            "validation_steps":
                validation_steps,

            # Retry information.
            "attempt":
                attempt + 1,

            "max_retries":
                self.retry_manager.get_max_retries()
        }
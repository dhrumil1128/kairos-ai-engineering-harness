"""
File: core/healing/recursive_engine.py

Purpose:
Coordinate autonomous execution,
recovery,
validation,
and retries.

Why:

This is the central brain of
the recursive healing system.

Architecture:

FLOW:

WORKFLOW

Task Received
      ↓
Set Status → RUNNING
      ↓
Execute Task
      ↓
Success?
   /      \
 Yes      No
  ↓        ↓
SUCCESS   Execution Loop
            ↓
      Error Analyzer
            ↓
      Self Correction
            ↓
      Generate Repair Plan
            ↓
      Reviewer Agent
            ↓
       Tester Agent
            ↓
   Validation Passed?
       /        \
     Yes        No
      ↓          ↓
    Retry    New Repair Plan
      ↓          ↓
 Execute Task ←──┘
      ↓
 Success?
   /      \
 Yes      No
  ↓        ↓
SUCCESS   Max Retries?
            /      \
          Yes      No
           ↓        ↓
        FAILED    Retry Again
                    ↓
              Execution Loop

Future Versions:

V2:
- ReviewerAgent execution

V3:
- TesterAgent execution

V4:
- Automatic code patching

V5:
- Fully autonomous recovery
"""

from core.shared.constants import (
    MAX_RETRIES
)

from core.shared.enums import (
    TaskStatus
)

from core.shared.exceptions import (
    ExecutionError
)

from core.shared.schemas import (
    TaskSchema
)

from core.executor.executor import (
    Executor
)

from core.healing.execution_loop import (
    ExecutionLoop
)


class RecursiveEngine:
    """
    Core healing engine.
    """

    def __init__(
        self,
        max_retries: int = MAX_RETRIES
    ):
        """
        Initialize engine.
        """

        self.max_retries = (
            max_retries
        )

        self.executor = (
            Executor()
        )

        self.execution_loop = (
            ExecutionLoop()
        )

    def execute_task(
        self,
        task: TaskSchema
    ) -> TaskSchema:
        """
        Execute task with
        recursive recovery.
        """

        task.status = (
            TaskStatus.RUNNING
        )

        retry_count = 0

        while retry_count < (
            self.max_retries
        ):

            try:

                success = (
                    self.executor.execute(
                        task
                    )
                )

                if success:

                    task.status = (
                        TaskStatus.SUCCESS
                    )

                    return task

            except Exception as error:

                recovery = (
                    self.execution_loop.process_error(
                        str(error),
                        retry_count
                    )
                )

                # Retry limit hit.
                if (
                    recovery["status"]
                    == "failed"
                ):

                    task.status = (
                        TaskStatus.FAILED
                    )

                    raise ExecutionError(
                        "Recovery failed"
                    ) from error

                # Store recovery metadata.
                task.metadata[
                    "recovery"
                ] = recovery

                retry_count += 1

                continue

        task.status = (
            TaskStatus.FAILED
        )

        return task
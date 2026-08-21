"""
File: core/healing/retry_manager.py

Purpose:
Control retry behavior for
the recursive healing system.

Why:

Without retry limits,
autonomous systems can enter
infinite repair loops.

Architecture:

Execution Failure
        ↓
Retry Manager
        ↓
Retry Allowed?
      /     \
    Yes      No
     ↓        ↓
 Retry     Fail Task

Future Versions:

V2:
- Error-aware retries

V3:
- Adaptive retry policies

V4:
- Agent-specific retries

V5:
- Learning-based retries
"""


class RetryManager:
    """
    Manage retry policies.
    """

    def __init__(
        self,
        max_retries: int = 3
    ):
        """
        Initialize manager.
        """

        self.max_retries = (
            max_retries
        )

    def should_retry(
        self,
        attempt: int
    ) -> bool:
        """
        Determine whether
        another retry is allowed.
        """

        return (
            attempt
            <
            self.max_retries
        )

    def get_max_retries(
        self
    ) -> int:
        """
        Return configured
        retry limit.
        """

        return (
            self.max_retries
        )

    def get_retry_metadata(
        self,
        attempt: int
    ) -> dict:
        """
        Build retry metadata.

        Used by:
        - Recursive Engine
        - Execution Loop
        - Healing Reports
        """

        return {

            "current_attempt":
                attempt,

            "next_attempt":
                attempt + 1,

            "remaining_retries":
                max(
                    0,
                    self.max_retries
                    - attempt
                ),

            "max_retries":
                self.max_retries,

            "retry_allowed":
                self.should_retry(
                    attempt
                )
        }

    def reset(
        self
    ) -> int:
        """
        Future hook for
        stateful retry systems.

        V1:
        Stateless.
        """

        return 0
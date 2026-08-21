"""
File: core/executor/execution_history.py

Purpose:
Track execution history across KAIROS.

Why:

Enterprise systems require:

- Traceability
- Debugging
- Auditing
- Compliance

Architecture:

Executor
    ↓
Execution History
    ↓
Future Audit Logs
"""

# Timestamp generation.
from datetime import UTC, datetime

# Structured typing.
from typing import Dict, Any, List


class ExecutionHistory:
    """
    Stores execution history.

    Version 1:

    In-memory storage.

    Future:

    - SQLite
    - PostgreSQL
    - Event Store
    - Audit Pipeline
    """

    def __init__(self):
        """
        Initialize execution history.
        """

        self.records: List[Dict[str, Any]] = []

    def add_record(
        self,
        task_id: str,
        command: str,
        success: bool,
        return_code: int
    ) -> None:
        """
        Store execution record.

        Parameters:
            task_id:
                Associated task.

            command:
                Executed command.

            success:
                Execution result.

            return_code:
                OS exit code.
        """

        self.records.append(
            {
                "task_id": task_id,
                "command": command,
                "success": success,
                "return_code": return_code,
                "timestamp": datetime.now(UTC),
            }
        )

    def get_records(self) -> List[Dict[str, Any]]:
        """
        Return all execution records.
        """

        return self.records

    def count(self) -> int:
        """
        Return total record count.
        """

        return len(self.records)
"""
File: core/shared/schemas.py

Purpose:
Centralized data models used across KAIROS.

Why:
Schemas provide a contract between modules.

Without schemas:
- Agents exchange random dictionaries
- Data becomes inconsistent

With schemas:
- Data is validated
- Structure remains consistent
- Easier debugging and maintenance

Architecture:

Planner
   ↓
Task Schema
   ↓
Architect
   ↓
Coder
   ↓
Executor
"""

from datetime import datetime, UTC
from uuid import uuid4

# Pydantic is used for validation and serialization.
from pydantic import BaseModel, Field

# Shared task states used across KAIROS.
from core.shared.enums import TaskStatus


class TaskSchema(BaseModel):
    """
    Core task representation.

    Every major workflow inside KAIROS
    will eventually be represented as a task.
    """

    # Unique identifier for the task.
    id: str = Field(default_factory=lambda: str(uuid4()))

    # Human-readable task name.
    name: str

    # Detailed task description.
    description: str = ""

    # Current execution state.
    status: TaskStatus = TaskStatus.PENDING

    # Priority level.
    priority: int = 1

    # Timestamp when task was created.
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    # Timestamp when task was last updated.
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )
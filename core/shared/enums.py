"""
File: core/shared/enums.py

Purpose:
Centralized enumerations used throughout KAIROS.

Why:
Avoid magic strings and maintain consistency
across agents, execution, memory, security,
and runtime modules.

Architecture Position:

Agents
Memory
Security
Executor
Runtime
        ↓
      Enums
"""

from enum import Enum


class TaskStatus(str, Enum):
    """
    Lifecycle status of a task.
    """

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    RETRYING = "RETRYING"


class AgentStatus(str, Enum):
    """
    Current state of an agent.
    """

    IDLE = "IDLE"
    WORKING = "WORKING"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"


class SecurityLevel(str, Enum):
    """
    Risk classification used by Glasswing.
    """

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ExecutionResult(str, Enum):
    """
    Execution outcome.
    """

    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class MemoryTier(str, Enum):
    """
    Memory hierarchy used by KAIROS.
    """

    ACTIVE = "ACTIVE"
    PROJECT = "PROJECT"
    DREAM = "DREAM"
    ARCHIVE = "ARCHIVE"
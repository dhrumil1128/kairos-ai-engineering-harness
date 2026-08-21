"""
File: tests/unit/shared/test_enums.py

Purpose:
Unit tests for KAIROS enums.

Why:
Ensures enum values remain stable and consistent
across the platform.
"""

from core.shared.enums import (
    TaskStatus,
    AgentStatus,
    SecurityLevel,
    ExecutionResult,
    MemoryTier,
)


def test_task_status():
    assert TaskStatus.PENDING == "PENDING"
    assert TaskStatus.RUNNING == "RUNNING"
    assert TaskStatus.SUCCESS == "SUCCESS"
    assert TaskStatus.FAILED == "FAILED"


def test_agent_status():
    assert AgentStatus.IDLE == "IDLE"
    assert AgentStatus.WORKING == "WORKING"


def test_security_level():
    assert SecurityLevel.LOW == "LOW"
    assert SecurityLevel.CRITICAL == "CRITICAL"


def test_execution_result():
    assert ExecutionResult.SUCCESS == "SUCCESS"
    assert ExecutionResult.FAILURE == "FAILURE"


def test_memory_tier():
    assert MemoryTier.ACTIVE == "ACTIVE"
    assert MemoryTier.DREAM == "DREAM"
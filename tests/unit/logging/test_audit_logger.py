"""
File: tests/unit/logging/test_audit_logger.py

Purpose:
Unit tests for AuditLogger.

Why:
Verify audit events are stored correctly.

Architecture:

Security
    ↓
Executor
    ↓
Audit Logger
    ↓
Unit Tests
"""

# Audit logging layer under test.
from core.logging.audit_logger import (
    AuditLogger
)


def test_audit_logger_creation():
    """
    Verify audit logger initialization.
    """

    logger = AuditLogger()

    assert logger is not None


def test_log_event():
    """
    Verify event logging.
    """

    logger = AuditLogger()

    logger.log_event(
        event_type="SECURITY_CHECK",
        message="Command approved"
    )

    assert logger.count() == 1


def test_get_events():
    """
    Verify event retrieval.
    """

    logger = AuditLogger()

    logger.log_event(
        event_type="EXECUTION",
        message="Task executed"
    )

    events = logger.get_events()

    assert len(events) == 1

    assert (
        events[0]["event_type"]
        == "EXECUTION"
    )

    assert (
        events[0]["message"]
        == "Task executed"
    )


def test_multiple_events():
    """
    Verify multiple event storage.
    """

    logger = AuditLogger()

    logger.log_event(
        "SECURITY",
        "Command validated"
    )

    logger.log_event(
        "EXECUTION",
        "Command executed"
    )

    assert logger.count() == 2
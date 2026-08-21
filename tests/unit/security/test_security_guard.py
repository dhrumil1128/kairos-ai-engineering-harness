"""
File: tests/unit/security/test_security_guard.py

Purpose:
Unit tests for Glasswing Security Shield.

Why:
Verify dangerous commands are blocked
and safe commands are allowed.

Architecture:

Security Guard
       ↓
Validation Decision
       ↓
Unit Tests
"""

# Security layer under test.
from core.security.security_guard import SecurityGuard


def test_security_guard_creation():
    """
    Verify security guard initialization.
    """

    guard = SecurityGuard()

    assert guard is not None


def test_safe_command():
    """
    Verify safe commands are allowed.
    """

    guard = SecurityGuard()

    result = guard.validate_command(
        "echo hello"
    )

    assert result["allowed"] is True


def test_block_rm_rf():
    """
    Verify rm -rf is blocked.
    """

    guard = SecurityGuard()

    result = guard.validate_command(
        "rm -rf /"
    )

    assert result["allowed"] is False


def test_block_shutdown():
    """
    Verify shutdown command is blocked.
    """

    guard = SecurityGuard()

    result = guard.validate_command(
        "shutdown now"
    )

    assert result["allowed"] is False


def test_case_insensitive_detection():
    """
    Verify case-insensitive matching.
    """

    guard = SecurityGuard()

    result = guard.validate_command(
        "REMOVE-ITEM test.txt"
    )

    assert result["allowed"] is False
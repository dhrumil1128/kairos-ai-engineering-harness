"""
File: tests/unit/shared/test_exceptions.py

Purpose:
Unit tests for KAIROS custom exceptions.

Why:
Ensures all custom exceptions behave correctly and
inherit from KairosException.

Architecture:

Shared Exceptions
        ↓
Unit Tests
"""

from core.shared.exceptions import (
    KairosException,
    AgentExecutionError,
    SecurityViolation,
    MemoryError,
    MCPConnectionError,
    ExecutionError,
    TokenBudgetExceeded,
    ConfigurationError,
)


def test_base_exception():
    exception = KairosException("Base error")

    assert str(exception) == "Base error"
    assert exception.message == "Base error"


def test_agent_execution_error():
    exception = AgentExecutionError("Agent failed")

    assert isinstance(exception, KairosException)
    assert str(exception) == "Agent failed"


def test_security_violation():
    exception = SecurityViolation("Blocked command")

    assert isinstance(exception, KairosException)
    assert str(exception) == "Blocked command"


def test_memory_error():
    exception = MemoryError("Memory retrieval failed")

    assert isinstance(exception, KairosException)


def test_mcp_connection_error():
    exception = MCPConnectionError("MCP unavailable")

    assert isinstance(exception, KairosException)


def test_execution_error():
    exception = ExecutionError("Sandbox failed")

    assert isinstance(exception, KairosException)


def test_token_budget_exceeded():
    exception = TokenBudgetExceeded("Token limit exceeded")

    assert isinstance(exception, KairosException)


def test_configuration_error():
    exception = ConfigurationError("Invalid configuration")

    assert isinstance(exception, KairosException)
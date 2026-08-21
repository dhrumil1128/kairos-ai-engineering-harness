"""
File: core/shared/exceptions.py

Purpose:
Centralized exception definitions for KAIROS.

Why this exists:
Every module should raise structured exceptions
instead of generic Python exceptions.

Benefits:
- Cleaner logging
- Easier debugging
- Better recovery workflows
- More reliable recursive execution

Architecture Position:

Agents
Memory
Security
Executor
MCP
    ↓
Shared Exceptions
"""

from typing import Optional


class KairosException(Exception):
    """
    Base exception for all KAIROS-specific errors.

    Every custom exception in the platform should inherit
    from this class.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class AgentExecutionError(KairosException):
    """
    Raised when an agent fails during execution.
    """


class SecurityViolation(KairosException):
    """
    Raised when Glasswing Security blocks an action.
    """


class MemoryError(KairosException):
    """
    Raised when memory retrieval or storage fails.
    """


class MCPConnectionError(KairosException):
    """
    Raised when an MCP service becomes unavailable.
    """


class ExecutionError(KairosException):
    """
    Raised when sandbox execution fails.
    """


class TokenBudgetExceeded(KairosException):
    """
    Raised when token limits are exceeded.
    """


class ConfigurationError(KairosException):
    """
    Raised when application configuration is invalid.
    """
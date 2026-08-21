"""
File: tests/unit/shared/test_constants.py

Purpose:
Validate KAIROS global constants.

Why:
Ensures critical configuration values remain
consistent and valid across the platform.

Architecture:

Constants
    ↓
Unit Tests
"""

# Shared application constants.
from core.shared.constants import (
    APP_NAME,
    APP_VERSION,
    MAX_RETRIES,
    RETRY_DELAY_SECONDS,
    DEFAULT_TIMEOUT_SECONDS,
    MAX_CONCURRENT_TASKS,
    DEFAULT_TOKEN_BUDGET,
    MAX_CONTEXT_DOCUMENTS,
    MAX_MEMORY_RESULTS,
    MAX_COMMAND_LENGTH,
    DEFAULT_LOG_LEVEL,
)


def test_application_constants():
    """
    Verify application metadata.
    """

    assert APP_NAME == "KAIROS"
    assert APP_VERSION == "0.1.0"


def test_retry_configuration():
    """
    Verify recursive execution settings.
    """

    assert MAX_RETRIES > 0
    assert RETRY_DELAY_SECONDS >= 0


def test_runtime_configuration():
    """
    Verify runtime safety limits.
    """

    assert DEFAULT_TIMEOUT_SECONDS > 0
    assert MAX_CONCURRENT_TASKS > 0


def test_token_configuration():
    """
    Verify token engine limits.
    """

    assert DEFAULT_TOKEN_BUDGET > 0
    assert MAX_CONTEXT_DOCUMENTS > 0


def test_memory_configuration():
    """
    Verify memory retrieval limits.
    """

    assert MAX_MEMORY_RESULTS > 0


def test_security_configuration():
    """
    Verify security limits.
    """

    assert MAX_COMMAND_LENGTH > 0


def test_logging_configuration():
    """
    Verify logging defaults.
    """

    assert DEFAULT_LOG_LEVEL == "INFO"
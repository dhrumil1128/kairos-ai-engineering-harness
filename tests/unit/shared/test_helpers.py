"""
File: tests/unit/shared/test_helpers.py

Purpose:
Unit tests for KAIROS helper utilities.

Why:
Ensures shared utility functions behave correctly
before being used by other modules.

Architecture:

Helpers
   ↓
Unit Tests
"""

# Shared utility functions.
from core.shared.helpers import (
    generate_id,
    utc_now,
    safe_get,
)


def test_generate_id():
    """
    Verify unique ID generation.
    """

    first_id = generate_id()
    second_id = generate_id()

    assert first_id is not None
    assert second_id is not None
    assert first_id != second_id


def test_utc_now():
    """
    Verify UTC timestamp generation.
    """

    timestamp = utc_now()

    assert timestamp is not None
    assert timestamp.tzinfo is not None


def test_safe_get_existing_key():
    """
    Verify retrieving existing key.
    """

    data = {
        "name": "KAIROS"
    }

    result = safe_get(data, "name")

    assert result == "KAIROS"


def test_safe_get_missing_key():
    """
    Verify default value is returned.
    """

    data = {}

    result = safe_get(
        data,
        "missing_key",
        "default_value"
    )

    assert result == "default_value"
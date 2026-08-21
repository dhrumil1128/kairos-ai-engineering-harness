"""
File: core/shared/helpers.py

Purpose:
Common utility functions used throughout KAIROS.

Why:
Avoid duplicate utility code across modules.

Architecture:

Agents
Memory
Security
Executor
Runtime
        ↓
      Helpers

Production Note:

Only place generic reusable functions here.

Do NOT place business logic here.
"""

from datetime import UTC, datetime
from uuid import uuid4


def generate_id() -> str:
    """
    Generate a globally unique identifier.

    Returns:
        str:
            UUID string.
    """

    return str(uuid4())


def utc_now() -> datetime:
    """
    Generate a timezone-aware UTC timestamp.

    Returns:
        datetime:
            Current UTC timestamp.
    """

    return datetime.now(UTC)


def safe_get(data: dict, key: str, default=None):
    """
    Safely retrieve a value from a dictionary.

    Args:
        data:
            Source dictionary.

        key:
            Dictionary key.

        default:
            Fallback value.

    Returns:
        Any:
            Retrieved value or default.
    """

    return data.get(key, default)
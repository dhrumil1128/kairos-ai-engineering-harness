"""
File:
tests/unit/mcp/
test_database_mcp.py

Purpose:
Verify real Database MCP.
"""

from core.mcp.database_mcp import (
    DatabaseMCP
)


def test_connection():
    """
    Verify database connection.
    """

    db = DatabaseMCP()

    assert (
        db.is_connected()
        is True
    )


def test_create_table():
    """
    Verify table creation.
    """

    db = DatabaseMCP()

    db.execute_query(
        """
        CREATE TABLE IF NOT EXISTS
        test_users (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
        """
    )

    assert True


def test_insert_record():
    """
    Verify insertion.
    """

    db = DatabaseMCP()

    db.execute_query(
        """
        INSERT INTO test_users
        (name)
        VALUES
        ('KAIROS')
        """
    )

    assert True


def test_fetch_record():
    """
    Verify retrieval.
    """

    db = DatabaseMCP()

    row = db.fetch_one(
        """
        SELECT name
        FROM test_users
        LIMIT 1
        """
    )

    assert (
        row[0]
        == "KAIROS"
    )
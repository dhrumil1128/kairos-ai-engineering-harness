"""
Episodic Memory
---------------
History

Working Memory
--------------
Current State

Semantic Memory
---------------
Knowledge

Memory Router
-------------
Routes Between Them
"""


"""
File: core/memory/working_memory.py

Purpose:
Persistent working memory.

Stores active execution context.

Architecture:

Working Memory
      ↓
Database MCP
      ↓
SQLite

Future Versions:

V2:
- PostgreSQL

V3:
- Redis caching

V4:
- Context compression

V5:
- Distributed memory
"""

# Database MCP.
from core.mcp.database_mcp import (
    DatabaseMCP
)


class WorkingMemory:
    """
    Persistent working memory.
    """

    def __init__(self):
        """
        Initialize memory.
        """

        # Database connection.
        self.database = DatabaseMCP()

        # Create memory table.
        self.database.execute_query(
            """
            CREATE TABLE IF NOT EXISTS
            working_memory (
                key TEXT PRIMARY KEY,
                value TEXT
            )
            """
        )

    def store(
        self,
        key: str,
        value: str
    ) -> None:
        """
        Store value.
        """

        # Replace existing value.
        self.database.execute_query(
            f"""
            INSERT OR REPLACE
            INTO working_memory
            (key, value)
            VALUES
            ('{key}', '{value}')
            """
        )

    def retrieve(
        self,
        key: str
    ):
        """
        Retrieve value.
        """

        row = self.database.fetch_one(
            f"""
            SELECT value
            FROM working_memory
            WHERE key = '{key}'
            """
        )

        if row:
            return row[0]

        return None
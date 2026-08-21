"""
File: core/memory/episodic_memory.py

Purpose:
Persistent episodic memory.

Stores events and history.

Architecture:

Agent
    ↓
Episodic Memory
    ↓
Database MCP
    ↓
SQLite

Future Versions:

V2:
- PostgreSQL

V3:
- Event metadata

V4:
- Search support

V5:
- Long-term agent history
"""

# Database MCP.
from core.mcp.database_mcp import (
    DatabaseMCP
)


class EpisodicMemory:
    """
    Persistent episodic memory.
    """

    def __init__(self):
        """
        Initialize memory.
        """

        # Database connection.
        self.database = DatabaseMCP()

        # Create event table.
        self.database.execute_query(
            """
            CREATE TABLE IF NOT EXISTS
            episodic_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event TEXT
            )
            """
        )

    def add_event(
        self,
        event: str
    ) -> None:
        """
        Store event.
        """

        self.database.execute_query(
            f"""
            INSERT INTO episodic_memory
            (event)
            VALUES
            ('{event}')
            """
        )

    def get_latest_event(
        self
    ):
        """
        Retrieve latest event.
        """

        row = self.database.fetch_one(
            """
            SELECT event
            FROM episodic_memory
            ORDER BY id DESC
            LIMIT 1
            """
        )

        if row:
            return row[0]

        return None
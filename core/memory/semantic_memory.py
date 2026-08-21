"""
File: core/memory/semantic_memory.py

Purpose:
Persistent semantic memory.

Stores long-term knowledge.

Architecture:

Agent
    ↓
Semantic Memory
    ↓
Database MCP
    ↓
SQLite

Future Versions:

V2:
- PostgreSQL

V3:
- Embeddings

V4:
- pgvector

V5:
- Semantic Search
"""

# Database MCP.
from core.mcp.database_mcp import (
    DatabaseMCP
)


class SemanticMemory:
    """
    Persistent semantic memory.
    """

    def __init__(self):
        """
        Initialize memory.
        """

        # Database connection.
        self.database = DatabaseMCP()

        # Create knowledge table.
        self.database.execute_query(
            """
            CREATE TABLE IF NOT EXISTS
            semantic_memory (
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
        Store knowledge.
        """

        self.database.execute_query(
            f"""
            INSERT OR REPLACE
            INTO semantic_memory
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
        Retrieve knowledge.
        """

        row = self.database.fetch_one(
            f"""
            SELECT value
            FROM semantic_memory
            WHERE key = '{key}'
            """
        )

        if row:
            return row[0]

        return None
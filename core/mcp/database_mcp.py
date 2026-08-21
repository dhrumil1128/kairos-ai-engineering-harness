"""
File: core/mcp/database_mcp.py

Purpose:
Real Database MCP using SQLAlchemy.

Supports:

- SQLite (development)
- PostgreSQL (enterprise)

Future Versions:

V2:
- ORM Models

V3:
- Memory Persistence

V4:
- Agent State Storage

V5:
- Enterprise Database Layer
"""

# SQLAlchemy database engine.
from sqlalchemy import (
    create_engine,
    text
)


class DatabaseMCP:
    """
    Real Database MCP.
    """

    def __init__(
        self,
        database_url: str = (
            "sqlite:///kairos.db"
        )
    ):
        """
        Initialize database connection.
        """

        # Create database engine.
        self.engine = create_engine(
            database_url
        )

    def is_connected(
        self
    ) -> bool:
        """
        Verify database connection.
        """

        try:

            # Open connection.
            with self.engine.connect():

                return True

        except Exception:

            return False

    def execute_query(
        self,
        query: str
    ) -> None:
        """
        Execute SQL query.
        """

        # Open transaction.
        with self.engine.begin() as conn:

            # Execute SQL.
            conn.execute(
                text(query)
            )

    def fetch_one(
        self,
        query: str
    ):
        """
        Execute query and
        return first row.
        """

        with self.engine.connect() as conn:

            result = conn.execute(
                text(query)
            )

            return result.fetchone()
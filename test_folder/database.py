"""
Database connection module for the sample application.

This module contains database connection logic that is repeated
across multiple files in the codebase.
"""

import sqlite3
from typing import Optional, List, Dict, Any
import os


class DatabaseConnection:
    """Database connection handler with repeated connection logic."""

    def __init__(self, db_path: str = "app.db"):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        """Establish database connection."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            return self.connection
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return None

    def disconnect(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results."""
        conn = self.connect()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = [dict(row) for row in cursor.fetchall()]
            return results
        except sqlite3.Error as e:
            print(f"Query execution error: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def execute_update(self, query: str, params: tuple = ()) -> bool:
        """Execute an INSERT, UPDATE, or DELETE query."""
        conn = self.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Update execution error: {e}")
            return False
        finally:
            if conn:
                conn.close()


# This connection logic gets repeated in other files
def get_db_connection():
    """Get database connection - this pattern is repeated elsewhere."""
    db_path = os.getenv("DATABASE_URL", "app.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

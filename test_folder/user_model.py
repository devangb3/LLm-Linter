"""
User model for the sample application.

This module contains user-related data models and operations.
Note: This duplicates some database connection logic from database.py
"""

import sqlite3
import hashlib
from typing import Optional, Dict, Any
from datetime import datetime
import os


class User:
    """User model with embedded database operations."""

    def __init__(self, user_id: Optional[int] = None, username: str = "", email: str = "",
                 password_hash: str = "", created_at: Optional[str] = None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at or datetime.now().isoformat()

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA256 (should use more secure method)."""
        return hashlib.sha256(password.encode()).hexdigest()

    @classmethod
    def create_table(cls):
        """Create users table - duplicates connection logic."""
        db_path = os.getenv("DATABASE_URL", "app.db")
        conn = sqlite3.connect(db_path)  # Repeated connection logic
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            conn.commit()
        finally:
            conn.close()

    @classmethod
    def find_by_username(cls, username: str) -> Optional['User']:
        """Find user by username - duplicates connection logic."""
        db_path = os.getenv("DATABASE_URL", "app.db")
        conn = sqlite3.connect(db_path)  # Repeated connection logic
        conn.row_factory = sqlite3.Row
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return cls(
                    user_id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    password_hash=row['password_hash'],
                    created_at=row['created_at']
                )
            return None
        finally:
            conn.close()

    def save(self) -> bool:
        """Save user to database - duplicates connection logic."""
        db_path = os.getenv("DATABASE_URL", "app.db")
        conn = sqlite3.connect(db_path)  # Repeated connection logic
        try:
            cursor = conn.cursor()
            if self.user_id:
                # Update existing user
                cursor.execute("""
                    UPDATE users SET username=?, email=?, password_hash=?, created_at=?
                    WHERE id=?
                """, (self.username, self.email, self.password_hash, self.created_at, self.user_id))
            else:
                # Insert new user
                cursor.execute("""
                    INSERT INTO users (username, email, password_hash, created_at)
                    VALUES (?, ?, ?, ?)
                """, (self.username, self.email, self.password_hash, self.created_at))
                self.user_id = cursor.lastrowid
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            conn.close()

    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary."""
        return {
            'id': self.user_id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at
        }

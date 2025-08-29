"""
Authentication service for the sample application.

This module handles user authentication and session management.
Note: This also duplicates database connection logic.
"""

import sqlite3
import jwt
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from user_model import User


class AuthService:
    """Authentication service with mixed concerns."""

    SECRET_KEY = "sample_secret_key_not_secure"  # Should be from config
    JWT_EXPIRATION_HOURS = 24

    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with username and password."""
        # Duplicate database connection logic
        db_path = os.getenv("DATABASE_URL", "app.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, email, password_hash, created_at
                FROM users WHERE username = ?
            """, (username,))

            row = cursor.fetchone()
            if row and User.hash_password(password) == row['password_hash']:
                # Create JWT token
                token = AuthService._generate_token(row['id'])
                return {
                    'user': {
                        'id': row['id'],
                        'username': row['username'],
                        'email': row['email']
                    },
                    'token': token
                }
            return None
        finally:
            conn.close()

    @staticmethod
    def validate_token(token: str) -> Optional[Dict[str, Any]]:
        """Validate JWT token and return user info if valid."""
        try:
            payload = jwt.decode(token, AuthService.SECRET_KEY, algorithms=["HS256"])

            # Duplicate database query logic
            db_path = os.getenv("DATABASE_URL", "app.db")
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row

            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, username, email FROM users WHERE id = ?",
                             (payload['user_id'],))
                row = cursor.fetchone()

                if row:
                    return {
                        'id': row['id'],
                        'username': row['username'],
                        'email': row['email']
                    }
                return None
            finally:
                conn.close()

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None

    @staticmethod
    def _generate_token(user_id: int) -> str:
        """Generate JWT token for user."""
        expiration = datetime.utcnow() + timedelta(hours=AuthService.JWT_EXPIRATION_HOURS)
        payload = {
            'user_id': user_id,
            'exp': expiration,
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, AuthService.SECRET_KEY, algorithm="HS256")

    @staticmethod
    def register_user(username: str, email: str, password: str) -> bool:
        """Register new user - duplicates User model logic."""
        if User.find_by_username(username):
            return False  # User already exists

        password_hash = User.hash_password(password)
        user = User(username=username, email=email, password_hash=password_hash)

        return user.save()

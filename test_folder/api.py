"""
API endpoints for the sample application.

This module contains HTTP API endpoints that use the various services.
Note: This mixes HTTP handling with business logic.
"""

from flask import Flask, request, jsonify, g
import sqlite3
import os
from typing import Dict, Any
from auth_service import AuthService
from user_model import User

app = Flask(__name__)


@app.before_request
def before_request():
    """Setup database connection for each request."""
    g.db = sqlite3.connect(os.getenv("DATABASE_URL", "app.db"))
    g.db.row_factory = sqlite3.Row


@app.after_request
def after_request(response):
    """Close database connection after each request."""
    if hasattr(g, 'db'):
        g.db.close()
    return response


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login endpoint with inline validation."""
    data = request.get_json()

    # Inline validation logic
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400

    # Direct use of auth service
    result = AuthService.authenticate_user(data['username'], data['password'])

    if result:
        return jsonify({
            'message': 'Login successful',
            'user': result['user'],
            'token': result['token']
        })
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/api/auth/register', methods=['POST'])
def register():
    """Registration endpoint with duplicate validation."""
    data = request.get_json()

    # Duplicate validation logic
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Username, email, and password required'}), 400

    # Check if user exists - duplicate logic
    if User.find_by_username(data['username']):
        return jsonify({'error': 'Username already exists'}), 409

    # Register user
    if AuthService.register_user(data['username'], data['email'], data['password']):
        return jsonify({'message': 'User registered successfully'}), 201
    else:
        return jsonify({'error': 'Registration failed'}), 500


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID with inline database query."""
    # Inline database query instead of using model
    cursor = g.db.cursor()
    cursor.execute("SELECT id, username, email, created_at FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()

    if row:
        return jsonify({
            'id': row['id'],
            'username': row['username'],
            'email': row['email'],
            'created_at': row['created_at']
        })
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users with inline query."""
    # Inline database query
    cursor = g.db.cursor()
    cursor.execute("SELECT id, username, email, created_at FROM users ORDER BY created_at DESC")
    rows = cursor.fetchall()

    users = []
    for row in rows:
        users.append({
            'id': row['id'],
            'username': row['username'],
            'email': row['email'],
            'created_at': row['created_at']
        })

    return jsonify({'users': users})


@app.route('/api/posts', methods=['POST'])
def create_post():
    """Create post endpoint - demonstrates missing authentication middleware."""
    # Missing authentication check!
    data = request.get_json()

    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'error': 'Title and content required'}), 400

    # Inline database operation for posts table that might not exist
    cursor = g.db.cursor()
    cursor.execute("""
        INSERT INTO posts (title, content, user_id, created_at)
        VALUES (?, ?, ?, datetime('now'))
    """, (data['title'], data['content'], data.get('user_id', 1)))

    g.db.commit()

    return jsonify({'message': 'Post created successfully'}), 201


if __name__ == '__main__':
    # Create tables
    User.create_table()

    # This might create posts table on the fly
    with sqlite3.connect(os.getenv("DATABASE_URL", "app.db")) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                user_id INTEGER,
                created_at TEXT NOT NULL
            )
        """)

    app.run(debug=True)

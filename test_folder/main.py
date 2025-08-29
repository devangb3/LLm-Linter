"""
Main application entry point for the sample application.

This module demonstrates how all the components work together,
but also shows architectural issues like tight coupling and
mixed responsibilities.
"""

import os
import sys
from database import DatabaseConnection
from user_model import User
from auth_service import AuthService
from config import config


class Application:
    """Main application class with mixed responsibilities."""

    def __init__(self):
        self.db = DatabaseConnection()
        self.is_running = False

    def initialize(self):
        """Initialize the application with mixed setup logic."""
        print("🚀 Initializing Sample Application...")

        # Database setup mixed with application logic
        try:
            User.create_table()
            print("✅ Database tables created")

            # Create some sample data
            self._create_sample_data()
            print("✅ Sample data created")

        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            return False

        return True

    def _create_sample_data(self):
        """Create sample users - business logic mixed with data setup."""
        sample_users = [
            {"username": "admin", "email": "admin@example.com", "password": "admin123"},
            {"username": "user1", "email": "user1@example.com", "password": "password123"},
            {"username": "user2", "email": "user2@example.com", "password": "password123"}
        ]

        for user_data in sample_users:
            if not User.find_by_username(user_data["username"]):
                user = User(
                    username=user_data["username"],
                    email=user_data["email"],
                    password_hash=User.hash_password(user_data["password"])
                )
                user.save()
                print(f"   Created user: {user_data['username']}")

    def run_api_server(self):
        """Run the API server - importing and running Flask here."""
        print("🌐 Starting API server...")

        # Import here creates tight coupling
        from api import app

        try:
            print(f"📡 Server running on http://{config.API_HOST}:{config.API_PORT}")
            print("Press Ctrl+C to stop")
            self.is_running = True
            app.run(
                host=config.API_HOST,
                port=config.API_PORT,
                debug=config.API_DEBUG
            )
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
        except Exception as e:
            print(f"❌ Server error: {e}")
        finally:
            self.is_running = False

    def cleanup(self):
        """Cleanup resources."""
        if hasattr(self, 'db'):
            self.db.disconnect()
        print("🧹 Cleanup completed")


def print_banner():
    """Print application banner."""
    banner = """
    ╔══════════════════════════════════════════════╗
    ║             SAMPLE APPLICATION              ║
    ║   Demonstrating Architectural Patterns      ║
    ╚══════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main entry point."""
    print_banner()

    app = Application()

    try:
        # Initialize application
        if not app.initialize():
            print("❌ Application initialization failed")
            sys.exit(1)

        # Run the API server
        app.run_api_server()

    except KeyboardInterrupt:
        print("\n👋 Application interrupted by user")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
    finally:
        app.cleanup()


if __name__ == "__main__":
    main()

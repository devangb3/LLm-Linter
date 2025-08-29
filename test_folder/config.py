"""
Configuration module for the sample application.

This module contains configuration settings, some of which are
hardcoded and should be environment-based.
"""

import os


class Config:
    """Application configuration."""

    # Database settings (should be environment variables)
    DATABASE_URL = os.getenv("DATABASE_URL", "app.db")
    DATABASE_POOL_SIZE = 10
    DATABASE_TIMEOUT = 30

    # Security settings (hardcoded secrets are bad practice)
    SECRET_KEY = "hardcoded_secret_key_not_secure_at_all"
    JWT_SECRET = "another_hardcoded_secret_for_jwt"
    JWT_EXPIRATION_HOURS = 24

    # API settings
    API_HOST = "localhost"
    API_PORT = 5000
    API_DEBUG = True

    # Email settings (placeholder values)
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USERNAME = "your_email@gmail.com"
    SMTP_PASSWORD = "your_password"

    # File upload settings
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.pdf']

    # Logging settings
    LOG_LEVEL = "DEBUG"
    LOG_FILE = "app.log"

    # External API keys (should be in environment)
    EXTERNAL_API_KEY = "placeholder_api_key"
    PAYMENT_API_KEY = "placeholder_payment_key"

    @classmethod
    def is_development(cls):
        """Check if running in development mode."""
        return os.getenv("ENV", "development") == "development"

    @classmethod
    def is_production(cls):
        """Check if running in production mode."""
        return os.getenv("ENV", "development") == "production"


# Global config instance
config = Config()

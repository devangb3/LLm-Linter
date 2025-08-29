"""
Configuration module for the Coding Assistant.

This module handles configuration settings, primarily the Gemini API key.
The API key should be obtained from Google AI Studio and stored in a .env file.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for managing application settings."""

    def __init__(self):
        """Initialize configuration with environment variables."""
        self.gemini_api_key = self._get_gemini_api_key()

    def _get_gemini_api_key(self) -> str:
        """
        Retrieve the Gemini API key from environment variables.

        Returns:
            str: The Gemini API key

        Raises:
            ValueError: If the API key is not found or is empty
        """
        api_key = os.getenv('GEMINI_API_KEY')

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables. "
                "Please create a .env file in the project root with your "
                "Gemini API key from Google AI Studio."
            )

        return api_key.strip()

    @property
    def api_key(self) -> str:
        """Get the Gemini API key."""
        return self.gemini_api_key


# Global configuration instance
config = Config()

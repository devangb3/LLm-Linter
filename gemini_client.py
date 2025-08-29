"""
Gemini AI client module for the Coding Assistant.

This module handles communication with the Google Gemini AI API,
including prompt construction, API calls, and response processing.
"""

from google import genai
from google.genai import types
from config import config


class GeminiClient:
    """Client for interacting with Google's Gemini AI API."""

    def __init__(self):
        """Initialize the Gemini client with API key."""
        self.api_key = config.api_key
        self.client = genai.Client(api_key=self.api_key)        
        self.system_instruction = "You are an expert code reviewer and linter. Analyze the following multi-language codebase provided below. Identify high-level, cross-file patterns, potential areas for refactoring, and inconsistencies in coding style or logic. Do not suggest trivial fixes. Focus on architectural improvements or repeated code that could be abstracted. Provide 3-5 actionable suggestions. For each suggestion, specify the relevant file(s) and provide a clear explanation of the issue and your proposed improvement."
        # Generation configuration for consistent responses
        self.generation_config = types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            temperature=0.3,  # Lower temperature for more focused analysis
            )

    def get_suggestions(self, code_context: str) -> str:
        """
        Get AI-powered suggestions for code improvements.

        Args:
            code_context: Aggregated codebase content from analyzer

        Returns:
            str: Formatted suggestions from the AI model

        Raises:
            Exception: If API call fails
        """
        if not code_context.strip():
            return "❌ No code content provided for analysis."

        try:
            print("🤖 Analyzing codebase with Gemini AI...")
            print("⏳ This may take a moment depending on codebase size...")

            prompt = self._build_analysis_prompt(code_context)   

            response = self.client.models.generate_content(
                model="gemini-2.5-pro",
                config=self.generation_config,
                contents=[prompt]
            )

            if response and response.text:
                print("✅ Analysis complete!")
                return self._format_response(response.text)
            else:
                return "❌ No response received from Gemini API."

        except Exception as e:
            error_msg = f"❌ Error communicating with Gemini API: {str(e)}"
            print(error_msg)

            # Provide helpful troubleshooting information
            if "API_KEY" in str(e).upper():
                error_msg += "\n💡 Make sure your GEMINI_API_KEY is set correctly in the .env file."
            elif "quota" in str(e).lower():
                error_msg += "\n💡 You may have exceeded your API quota. Check your Google AI Studio dashboard."
            elif "network" in str(e).lower():
                error_msg += "\n💡 Check your internet connection and try again."

            return error_msg

    def _build_analysis_prompt(self, code_context: str) -> str:
        """
        Build the analysis prompt for the AI model.

        Args:
            code_context: The aggregated code content

        Returns:
            str: Complete prompt for the model
        """
        prompt = f"Codebase: {code_context}"
        return prompt

    def _format_response(self, response_text: str) -> str:
        """
        Format the AI response for better readability.

        Args:
            response_text: Raw response from the model

        Returns:
            str: Formatted response with better structure
        """
        # Add header decoration
        formatted_response = "\n" + "="*80 + "\n"
        formatted_response += "🎯 CODE ANALYSIS RESULTS\n"
        formatted_response += "="*80 + "\n\n"

        # Clean up the response text
        formatted_response += response_text.strip()

        # Add footer
        formatted_response += "\n\n" + "="*80 + "\n"
        formatted_response += "✨ Analysis powered by Google Gemini AI\n"
        formatted_response += "="*80 + "\n"

        return formatted_response

    def validate_api_key(self) -> bool:
        """
        Validate that the API key is working by making a simple test call.

        Returns:
            bool: True if API key is valid, False otherwise
        """
        try:
            # Make a simple test request
            test_prompt = "Hello, can you respond with 'API key is working' if you receive this message?"
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[test_prompt]
            )

            if response and response.text:
                return True
            return False

        except Exception:
            return False

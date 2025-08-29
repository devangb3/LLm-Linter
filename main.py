#!/usr/bin/env python3
"""
Coding Assistant - AI-Powered Code Analysis Tool

A command-line tool that analyzes codebases using Google Gemini AI to provide
actionable suggestions for improvements, refactoring opportunities, and
architectural enhancements.

Usage:
    python main.py --path /path/to/your/codebase

Requirements:
- Google Gemini API key (set in .env file as GEMINI_API_KEY)
- Python packages: google-generativeai, python-dotenv
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

from analyzer import CodeAnalyzer
from gemini_client import GeminiClient
from config import config


class CodingAssistant:
    """Main application class for the Coding Assistant."""

    def __init__(self):
        """Initialize the coding assistant."""
        self.analyzer = CodeAnalyzer()
        self.gemini_client = GeminiClient()

    def run(self, directory_path: str) -> int:
        """
        Run the complete analysis workflow.

        Args:
            directory_path: Path to the directory to analyze

        Returns:
            int: Exit code (0 for success, 1 for error)
        """
        try:
            self._print_header()

            if not self._validate_environment():
                return 1

            print(f"\nTarget directory: {directory_path}")
            code_context = self.analyzer.analyze_codebase(directory_path)

            if not code_context:
                print("No analyzable code found. Please check the directory path.")
                return 1

            suggestions = self.gemini_client.get_suggestions(code_context)

            print(suggestions)

            self._save_suggestions_to_file(suggestions, directory_path)

            return 0

        except KeyboardInterrupt:
            print("\n\nAnalysis interrupted by user.")
            return 1
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            return 1

    def _print_header(self):
        """Print the application header."""
        header = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                           🤖 CODING ASSISTANT                             ║
║                      AI-Powered Code Analysis Tool                         ║
║                                                                            ║
║  Analyze your codebase for patterns, improvements, and refactoring         ║
║  opportunities using Google's Gemini AI                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        print(header)

    def _validate_environment(self) -> bool:
        """
        Validate the environment setup.

        Returns:
            bool: True if environment is valid, False otherwise
        """
        print("🔧 Validating environment...")

        try:
            config.api_key
            print("API key found")
        except ValueError as e:
            print(f"{e}")
            return False

        print("Testing API connection...")
        if self.gemini_client.validate_api_key():
            print("API connection successful")
        else:
            print("API connection failed. Please check your API key.")
            return False

        return True

    def _save_suggestions_to_file(self, suggestions: str, directory_path: str) -> None:
        """
        Save the analysis suggestions to a timestamped file.

        Args:
            suggestions: The AI suggestions to save
            directory_path: The analyzed directory path (for metadata)
        """
        try:
            output_dir = Path("analysis_output")
            output_dir.mkdir(exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"analysis_{timestamp}.txt"
            filepath = output_dir / filename

            content = f"""Coding Assistant Analysis Report
                        {'='*50}
                        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                        Analyzed Directory: {directory_path}
                        {'='*50}

                        {suggestions}

                        {'='*50}
                        End of Analysis Report
                        """

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"\nAnalysis saved to: {filepath}")

        except Exception as e:
            print(f" Warning: Could not save analysis to file: {e}")


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="AI-powered code analysis tool using Google Gemini",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --path /home/user/my-project
  python main.py --path ./src
  python main.py --path ../backend

Environment Setup:
  1. Get your Gemini API key from Google AI Studio
  2. Create a .env file in the project root
  3. Add: GEMINI_API_KEY=your_api_key_here
        """
    )

    parser.add_argument(
        '--path',
        required=True,
        help='Path to the directory containing source code to analyze'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='Coding Assistant v1.0.0'
    )

    return parser.parse_args()


def main() -> int:
    """
    Main entry point for the application.

    Returns:
        int: Exit code
    """
    try:
        args = parse_arguments()

        directory_path = Path(args.path).resolve()

        if not directory_path.exists():
            print(f"Error: Directory '{args.path}' does not exist.")
            print(f"Absolute path: {directory_path}")
            return 1

        if not directory_path.is_dir():
            print(f"Error: '{args.path}' is not a directory.")
            return 1

        assistant = CodingAssistant()
        return assistant.run(str(directory_path))

    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        return 0
    except Exception as e:
        print(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

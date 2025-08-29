"""
Code analyzer module for the Coding Assistant.

This module handles scanning a directory for source code files,
reading their contents, and aggregating them into a single context
for AI analysis.
"""

import os
from pathlib import Path
from typing import List, Set


class CodeAnalyzer:
    """Handles codebase analysis and content aggregation."""

    # Common source code file extensions to analyze
    SUPPORTED_EXTENSIONS = {
        '.py',   # Python
        '.js',   # JavaScript
        '.ts',   # TypeScript
        '.jsx',  # React JavaScript
        '.tsx',  # React TypeScript
        '.go',   # Go
        '.java', # Java
        '.cs',   # C#
        '.cpp',  # C++
        '.c',    # C
        '.rb',   # Ruby
        '.rs',   # Rust
        '.php',  # PHP
        '.kt',   # Kotlin
        '.swift', # Swift
        '.scala', # Scala
    }

    # Directories to ignore during scanning
    IGNORED_DIRECTORIES = {
        '__pycache__',
        '.venv',
        'venv',
        '.env',
        '.git',
        'node_modules',
        '.next',
        'dist',
        'build',
        'target',
        '.gradle',
        '.idea',
        '.vscode',
        '.pytest_cache',
        '.mypy_cache',
        '.tox',
        'htmlcov',
        '.coverage',
        '.DS_Store',
    }

    def __init__(self):
        """Initialize the code analyzer."""
        self.files_analyzed = 0
        self.total_size = 0

    def analyze_codebase(self, directory_path: str) -> str:
        """
        Analyze a codebase directory and return aggregated content.

        Args:
            directory_path: Path to the directory to analyze

        Returns:
            str: Aggregated content of all source files

        Raises:
            FileNotFoundError: If the directory doesn't exist
            PermissionError: If there's no permission to read files
        """
        directory = Path(directory_path)

        if not directory.exists():
            raise FileNotFoundError(f"Directory '{directory_path}' does not exist")

        if not directory.is_dir():
            raise ValueError(f"'{directory_path}' is not a directory")

        print(f"🔍 Scanning directory: {directory_path}")
        print(f"📁 Supported file types: {', '.join(sorted(self.SUPPORTED_EXTENSIONS))}")

        # Find all source files
        source_files = self._find_source_files(directory)

        if not source_files:
            print("⚠️  No source files found in the specified directory")
            return ""

        print(f"📄 Found {len(source_files)} source files")

        # Aggregate content from all files
        aggregated_content = self._aggregate_file_contents(source_files)

        print("✅ Codebase analysis complete!")
        print(f"   Files analyzed: {self.files_analyzed}")
        print(f"   Total size: {self._format_file_size(self.total_size)}")

        return aggregated_content

    def _find_source_files(self, directory: Path) -> List[Path]:
        """
        Recursively find all source files in the directory.

        Args:
            directory: Directory to search in

        Returns:
            List[Path]: List of source file paths
        """
        source_files = []

        for root, dirs, files in os.walk(directory):
            # Filter out ignored directories
            dirs[:] = [d for d in dirs if d not in self.IGNORED_DIRECTORIES]

            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                    source_files.append(file_path)

        return source_files

    def _aggregate_file_contents(self, file_paths: List[Path]) -> str:
        """
        Aggregate contents of multiple files into a single string.

        Args:
            file_paths: List of file paths to read

        Returns:
            str: Aggregated content with file headers
        """
        aggregated_parts = []

        for file_path in file_paths:
            try:
                content = self._read_file_content(file_path)
                if content:  # Only add non-empty files
                    relative_path = file_path.relative_to(file_path.parents[-1])
                    file_header = f"\n{'='*80}\n"
                    file_header += f"FILE: {relative_path}\n"
                    file_header += f"LANGUAGE: {self._get_language_from_extension(file_path.suffix)}\n"
                    file_header += f"{'='*80}\n\n"

                    aggregated_parts.append(file_header + content)
                    self.files_analyzed += 1
                    self.total_size += len(content.encode('utf-8'))

            except (PermissionError, UnicodeDecodeError) as e:
                print(f"⚠️  Skipping {file_path}: {e}")
                continue

        return "\n".join(aggregated_parts)

    def _read_file_content(self, file_path: Path) -> str:
        """
        Read content from a single file.

        Args:
            file_path: Path to the file to read

        Returns:
            str: File content

        Raises:
            PermissionError: If file cannot be read
            UnicodeDecodeError: If file is not valid text
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Skip files that are too large (over 1MB) to avoid token limits
            if len(content.encode('utf-8')) > 1024 * 1024:
                print(f"⚠️  Skipping large file: {file_path} (>1MB)")
                return ""

            return content

        except (PermissionError, UnicodeDecodeError):
            raise

    def _get_language_from_extension(self, extension: str) -> str:
        """
        Get programming language name from file extension.

        Args:
            extension: File extension (with dot)

        Returns:
            str: Programming language name
        """
        language_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.jsx': 'React JavaScript',
            '.ts': 'TypeScript',
            '.tsx': 'React TypeScript',
            '.go': 'Go',
            '.java': 'Java',
            '.cs': 'C#',
            '.cpp': 'C++',
            '.c': 'C',
            '.rb': 'Ruby',
            '.rs': 'Rust',
            '.php': 'PHP',
            '.kt': 'Kotlin',
            '.swift': 'Swift',
            '.scala': 'Scala',
        }

        return language_map.get(extension.lower(), 'Unknown')

    def _format_file_size(self, size_bytes: int) -> str:
        """
        Format file size in human-readable format.

        Args:
            size_bytes: Size in bytes

        Returns:
            str: Formatted size string
        """
        if size_bytes < 1024:
            return f"{size_bytes} bytes"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"

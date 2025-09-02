# Coding Assistant

An AI-powered command-line tool that analyzes your codebase using Google's Gemini AI to provide actionable suggestions for improvements, refactoring opportunities, and architectural enhancements.
Add new change
## Features

- **Multi-language Support**: Analyzes Python, JavaScript, TypeScript, Go, Java, C#, C++, C, Ruby, Rust, PHP, Kotlin, Swift, and Scala
- **Cross-file Analysis**: Identifies patterns and relationships across your entire codebase
- **AI-Powered Insights**: Uses Google's Gemini AI for intelligent code analysis
- **Architectural Focus**: Focuses on high-level improvements rather than trivial fixes
- **Command-line Interface**: Simple, fast CLI tool with no GUI dependencies
- **Smart Filtering**: Automatically ignores common directories and binary files

## Quick Start

### 1. Prerequisites

- Python 3.9+
- Google Gemini API key (get one from [Google AI Studio](https://aistudio.google.com/app/apikey))

### 2. Installation

```bash
# Clone or download the project
cd /path/to/coding-assistant

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy the example environment file
cp env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here
```

### 4. Usage

```bash
# Analyze a codebase
python main.py --path /path/to/your/project

# Get help
python main.py --help

# Examples
python main.py --path ./src
python main.py --path ../backend
python main.py --path /home/user/my-web-app
```

## 📋 What It Analyzes

The tool scans your directory for source code files with these extensions:
- `.py` - Python
- `.js`, `.jsx` - JavaScript/React
- `.ts`, `.tsx` - TypeScript/React
- `.go` - Go
- `.java` - Java
- `.cs` - C#
- `.cpp`, `.c` - C/C++
- `.rb` - Ruby
- `.rs` - Rust
- `.php` - PHP
- `.kt` - Kotlin
- `.swift` - Swift
- `.scala` - Scala

## Analysis Focus

The AI analyzes your codebase for:

- **Cross-file Patterns**: Repeated code that could be abstracted
- **Architectural Improvements**: Better organization and structure
- **Refactoring Opportunities**: Code that could be simplified or restructured
- **Consistency Issues**: Inconsistent coding styles or patterns
- **High-level Design**: Overall system architecture improvements

**Note**: The tool focuses on architectural and design improvements, not trivial fixes like formatting or minor optimizations.

## Directory Structure

```
coding-assistant/
├── main.py              # CLI entry point
├── analyzer.py          # Codebase scanning and analysis
├── gemini_client.py     # Gemini AI API client
├── config.py            # Configuration management
├── requirements.txt     # Python dependencies
├── env.example          # Environment setup template
└── README.md           # This file
```

## 🔧 Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### Ignored Directories

The tool automatically ignores these common directories:
- `__pycache__`, `.venv`, `venv`
- `.git`, `node_modules`
- `.next`, `dist`, `build`
- `.gradle`, `.idea`, `.vscode`
- Various test and cache directories

### File Size Limits

- Individual files larger than 1MB are skipped
- Total analysis is capped for API token limits

## 🛠️ Troubleshooting

### API Key Issues
```bash
GEMINI_API_KEY not found in environment variables
```
**Solution**: Make sure your `.env` file exists and contains a valid API key from Google AI Studio.

### Network Issues
```bash
Error communicating with Gemini API
```
**Solution**: Check your internet connection and API quota limits in Google AI Studio.

### No Files Found
```bash
No source files found in the specified directory
```
**Solution**: Verify the path contains supported source code files and check that they're not in ignored directories.

### Permission Errors
```bash
Error: Permission denied
```
**Solution**: Make sure you have read access to the target directory and files.

## Output Files

The tool automatically saves analysis results to timestamped files in the `analysis_output/` directory:

### File Naming Convention
- Format: `analysis_YYYYMMDD_HHMMSS.txt`
- Example: `analysis_20241215_143052.txt`

### File Content Structure
```
Coding Assistant Analysis Report
==================================================
Generated: 2024-12-15 14:30:52
Analyzed Directory: /path/to/project
==================================================

[AI Analysis Results Here]

==================================================
End of Analysis Report
```

### Managing Output Files
```bash
# View all analysis reports
ls analysis_output/

# Read latest analysis
cat analysis_output/$(ls analysis_output/ | tail -1)

# Clean old reports (keep last 10)
cd analysis_output && ls -t | tail -n +11 | xargs rm -f
```

## 📊 Example Output

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                           🤖 CODING ASSISTANT                             ║
║                      AI-Powered Code Analysis Tool                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

Validating environment...
API key found
Testing API connection...
API connection successful

Target directory: /path/to/project
Scanning directory: /path/to/project
Supported file types: .py, .js, .ts, .go, .java, .cs, .cpp, .c, .rb, .rs
Found 25 source files

Analyzing codebase with Gemini AI...
This may take a moment depending on codebase size...
Analysis complete!

================================================================================
CODE ANALYSIS RESULTS
================================================================================

1. **Database Connection Abstraction**
   Files: database.py, models/user.py, services/auth.py

   The database connection logic is repeated across multiple files.
   Consider creating a centralized database connection manager...

[Additional suggestions...]

```

## Fututre Improvements

This is an MVP implementation. Potential enhancements:
- Support for additional file types
- Configuration file for custom analysis rules
- Output formatting options (JSON, HTML)
- Integration with CI/CD pipelines
- Caching of analysis results

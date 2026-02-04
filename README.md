# AI Agent

An AI-powered coding agent that can interact with your filesystem, execute Python files, and perform various file operations within a sandboxed working directory.

## Overview

This project implements an AI agent using Google's Gemini API that can autonomously perform file operations and execute Python code. The agent has access to a set of predefined functions that allow it to:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All operations are scoped to a specific working directory (`./calculator` by default) for security purposes.

## Features

- **Filesystem Operations**: List, read, and write files within the working directory
- **Python Execution**: Run Python files with arguments and capture their output
- **Path Security**: Automatic validation to prevent directory traversal attacks
- **Function Calling**: Uses Gemini's function calling capability to autonomously decide which operations to perform
- **Iterative Processing**: Agent can make up to 20 function calls to complete complex tasks

## Installation

1. Ensure you have Python 3.13 installed (as specified in [.python-version](.python-version))

2. Install dependencies:

```sh
uv sync
```

3. Create a `.env` file with your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

## Usage

Run the agent with a user prompt:

```sh
python main.py "your prompt here"
```

Enable verbose output to see detailed function calls and token usage:

```sh
python main.py "your prompt here" --verbose
```

### Example Prompts

```sh
python main.py "List all files in the calculator directory"
python main.py "Read the calculator.py file and explain what it does"
python main.py "Run the tests.py file and show me the results"
python main.py "Create a new file called notes.txt with some example content"
```

## Project Structure

```
.
├── main.py                          # Main entry point for the AI agent
├── config.py                        # Configuration (max file read size)
├── prompts.py                       # System prompt for the AI agent
├── call_function.py                 # Function calling orchestration
├── functions/                       # Available functions for the agent
│   ├── get_files_info.py           # List files and directories
│   ├── get_file_content.py         # Read file contents
│   ├── run_python_file.py          # Execute Python files
│   └── write_file.py               # Write/overwrite files
├── calculator/                      # Example working directory
│   ├── main.py                     # Calculator CLI application
│   ├── tests.py                    # Unit tests
│   └── pkg/
│       ├── calculator.py           # Calculator implementation
│       └── render.py               # JSON output formatter
└── test_*.py                       # Manual test files for each function
```

## Available Functions

### 1. `get_files_info`

Lists files in a directory with size and type information.

**Parameters:**

- `directory` (optional): Directory path relative to working directory (default: ".")

### 2. `get_file_content`

Reads and returns file contents (truncated at 10,000 characters).

**Parameters:**

- `file_path` (required): File path relative to working directory

### 3. `run_python_file`

Executes a Python file and captures its output.

**Parameters:**

- `file_path` (required): Python file path relative to working directory
- `args` (optional): Array of command-line arguments

### 4. `write_file`

Writes content to a file, creating parent directories if needed.

**Parameters:**

- `file_path` (required): File path relative to working directory
- `content` (required): Content to write to the file

## Security Features

- **Path Validation**: All file paths are validated to prevent directory traversal attacks
- **Working Directory Scoping**: All operations are restricted to the configured working directory
- **File Type Checking**: Python execution only allowed on `.py` files
- **Timeout Protection**: Python execution has a 30-second timeout limit

## Configuration

- [`MAX_CHARS`](config.py): Maximum characters to read from a file (default: 10,000)
- Working directory is hardcoded to `./calculator` in [`call_function.py`](call_function.py)

## Testing

Manual test files are provided for each function:

```sh
python test_get_files_info.py
python test_get_file_content.py
python test_run_python_file.py
python test_write_file.py
```

## Example: Calculator Application

The project includes a sample calculator application in the [`calculator/`](calculator/) directory that demonstrates the agent's capabilities:

- Expression evaluation with operator precedence
- JSON output formatting
- Unit tests
- CLI interface

Run the calculator directly:

```sh
python calculator/main.py "3 + 5 * 2"
```

Or ask the agent to interact with it:

```sh
python main.py "Run the calculator with the expression '10 * 5 + 3'"
```

## Dependencies

- [`google-genai`](pyproject.toml): Google Gemini API client
- [`python-dotenv`](pyproject.toml): Environment variable management

## License

This project is for educational purposes.

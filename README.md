

# Function Calling Chatbot

A lightweight AI-powered chatbot built from scratch in Python that uses function calling to interact with the local system.

## Features

The chatbot can use function calls to:

* Read files from disk
* Write files to disk
* Retrieve file contents
* Execute Python scripts
* Interact with the user through natural language prompts

The model decides when to invoke a function and automatically uses the appropriate tool to complete the user's request.

## Usage

Display help:

```
source .venv/bin/activate
```

```bash
python -m main --help
```

Output:

```text
usage: main.py [-h] [--verbose] user_prompt

Chatbot

positional arguments:
  user_prompt  User prompt

options:
  -h, --help   show this help message and exit
  --verbose    Enable verbose output
```

Run a prompt:

```bash
python -m main "List all Python files in the current directory"
```

Enable verbose mode:

```bash
python -m main --verbose "Read config.json and summarize it"
```

## Examples

Read a file:

```bash
python -m main "Read README.md"
```

Write a file:

```bash
python -m main "Create notes.txt containing Hello World"
```

Execute a Python script:

```bash
python -m main "Run script.py"
```

## Architecture

The project is built from scratch and consists of:

* A command-line interface (CLI)
* A function-calling framework
* Tool implementations for filesystem access and Python execution
* A conversation loop that routes model requests to local functions

## Warning

The application can read, modify, and execute files on the local machine. Only use it in trusted environments and review any actions before granting execution permissions.


Built during a course on boot.dev as a learning project demonstrating how modern LLM function calling can be integrated with local tooling.
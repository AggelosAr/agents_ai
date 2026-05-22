TOOLS = [
    {
        "type": "function",
        "name": "get_file_content",
        "description": "Get the contents of the desired file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "file_path": "The file path.",
                },
            },
            "required": ["file_path"],
        },
    },
    {
        "type": "function",
        "name": "write_file",
        "description": "Write or overwrite the file contents with the new.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file that its' content will be updated.",
                },
                "content": {
                    "type": "string",
                    "description": "The content to update the file with.",
                },
            },
            "required": ["file_path", "content"],
        },
    },
    {
        "type": "function",
        "name": "run_python_file",
        "description": "Run a python file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_name": {
                    "type": "string",
                    "description": "The path of the file to run.",
                },
                "args": {
                    "type": "string",
                    "description": "The args to pass to the python excecutable.",
                },
            },
            "required": ["file_name", "args"],
        },
    },
    {
        "type": "function",
        "name": "get_files_info",
        "description": "Get folder and file information.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The directory to search for the files or folders metadata.",
                },
            },
            "required": ["directory"],
        },
    }, 
]


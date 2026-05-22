

TOOLS = [
    {
        "type": "function",
        "name": "get_files_info",
        "description": "Get folder and file informations.",
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


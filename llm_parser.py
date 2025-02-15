import os, json, re

from AIProxy import get_completions, get_tool_completions

# Define the predefined task descriptions
function_definitions_llm = [
    {
        "name": "A1",
        "description": "Run a Python script from a given git URL, passing an email as the argument.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "pattern": r"https://raw.githubusercontent.com*\.py"},
                "targetfile": {"type": "string", "pattern": r".*/(.*\.py)"},
                "email": {"type": "string", "pattern": r"[\w\.-]+@[\w\.-]+\.\w+"}
            },
            "required": ["filename", "targetfile", "email"]
        }
    },
    {
        "name": "A2",
        "description": "Format a markdown file using Prettier.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "pattern": r"/data/(.*\.md)"},
                "targetfile": {"type": "string", "pattern": r"/data/(.*\.md)"}
            },
            "required": ["filename", "targetfile"]
        }
    },
    {
        "name": "A3",
        "description": "Count the number of occurrences of a specific weekday in a date file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "pattern": r"/data/(.*\.txt)"},
                "targetfile": {"type": "string", "pattern": r"/data/(.*\.txt)"},
                "weekday": {"type": "integer", "description": "weekday as per python datetime module (0=Monday, 1=Tuesday, ..., 6=Sunday)"}
            },
            "required": ["filename", "targetfile", "weekday"]
        }
    },
    {
        "name": "A4",
        "description": "Sort data in a JSON file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "pattern": r"/data/(.*\.json)"},
                "targetfile": {"type": "string", "pattern": r"/data/(.*\.json)"},
                "sorting_fields": {"type": "array", "items": {"type": "string", "pattern": r"\w+"}}
            },
            "required": ["filename", "targetfile", "sorting_fields"]
        }
    },
    {
        "name": "A5",
        "description": "Extract the 'x' line(s) from 'n' log files.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "pattern": r"/data/\w+"},
                "targetfile": {"type": "string", "pattern": r"/data/(.*\.json)"},
                "num_files": {"type": "integer", "pattern": r"\d+"},
                "num_lines": {"type": "integer", "pattern": r"\d+", "default": 1},
                "order": {"type": "string", "pattern": r"(asc|desc)", "default": "desc"}
            },
            "required": ["filename", "targetfile", "num_files"]
        }
    },
    {
        "name": "A6",
        "description": "Extract specific elements from Markdown (.md) files from directory and generate an index mapping filenames to extracted content.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "pattern": r"^/data/\w+", "description": "Markdown directory path."},
                "targetfile": {"type": "string", "pattern": r"^/data/(.*\.json)"},
                "extract": {"type": "string", "pattern": r"(h1|h2|h3|h4|h5|h6)", "default": "h1"}
            },
            "required": ["filename", "targetfile"]
        }
    },
    {
        "name": "A7",
        "description": "Extract the sender's email from an email file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "pattern": r"/data/(.*\.txt)"},
                "targetfile": {"type": "string", "pattern": r"/data/(.*\.txt)"}
            },
            "required": ["filename", "targetfile"]
        }
    },
    {
        "name": "A8",
        "description": "Extract a credit card number from an image.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "pattern": r"/data/(.*\.(png|jpg|jpeg))"},
                "targetfile": {"type": "string", "pattern": r"/data/(.*\.txt)"}
            },
            "required": ["filename", "targetfile"]
        }
    },
    {
        "name": "A9",
        "description": "Find the most similar pair of comments.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "pattern": r"/data/(.*\.txt)"},
                "targetfile": {"type": "string", "pattern": r"/data/(.*\.txt)"}
            },
            "required": ["filename", "targetfile"]
        }
    },
    {
        "name": "A10",
        "description": "Compute total sales for a specific ticket type in an SQLite database.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "pattern": r"/data/(.*\.db)"},
                "targetfile": {"type": "string", "pattern": r"/data/(.*\.txt)"},
                "expression": {"type": "string", "description": "complete SQL query."}
            },
            "required": ["filename", "targetfile", "expression"]
        }
    },
    {
        "name": "B3",
        "description": "Fetch data from an API and save it",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "pattern": r"https?://[^\s]+"},
                "targetfile": {"type": "string", "pattern": r"/[\w\-/]+(?:\.\w+)?"}
            },
            "required": ["filename", "targetfile"]
        }
    },
    {
        "name": "B4",
        "description": "Clone a Git repository and make a commit.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "pattern": r"https?://[\w./-]+\.git"}
            },
            "required": ["filename"]
        }
    },
    {
        "name": "B5",
        "description": "Run a SQL query on a SQLite or DuckDB database and write the result to a target file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "pattern": r"/[\w\-/]+\.db|/[\w\-/]+\.duckdb"},
                "targetfile": {"type": "string", "pattern": r"/[\w\-/]+\.\w+"},
                "query": {"type": "string", "pattern": r".*"}
            },
            "required": ["filename", "targetfile", "query"]
        }
    },
    {
        "name": "B6",
        "description": "Extract data/scrape data from a website",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "pattern": r"https?://[^\s]+"},
                "targetfile": {"type": "string", "pattern": r"/[\w\-/]+\.\w+"}
            },
            "required": ["filename", "targetfile"]
        }
    },
    {
        "name": "B7",
        "description": "Compress or resize an image and save it to output path.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "pattern": r"/[\w\-/]+\.(jpg|jpeg|png|webp)"},
                "targetfile": {"type": "string", "pattern": r"/[\w\-/]+\.(jpg|jpeg|png|webp)"},
                "resize": 
                    {"type": "object", "properties": 
                        {"width": {"type": "integer", "pattern": r"\d+"}, "height": {"type": "integer", "pattern": r"\d+"}}
                    },
                "quality": {"type": "integer", "pattern": r"\d+", "default": 100}
            },
            "required": ["filename", "targetfile"]
        }
    },
    {
        "name": "B9",
        "description": "Convert a Markdown (.md) file to an HTML (.html) file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "pattern": r"/[\w\-/]+\.md"},
                "targetfile": {"type": "string", "pattern": r"/[\w\-/]+\.html"}
            },
            "required": ["filename", "targetfile"]
        }
    },
    {
        "name": "B10",
        "description": "API endpoint that filters a CSV file and returns JSON data",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "pattern": r"/[\w\-/]+\.csv"},
                "targetfile": {"type": "string", "pattern": r"/[\w\-/]+\.json"},
                "filters": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "column": {"type": "string", "pattern": r"\w+"},
                            "value": {"type": "string", "pattern": r"\w+"}
                        },
                        "required": ["column", "value"]
                    }
                }
            },
            "required": ["filename", "targetfile"]
        }
    },
    {
        "name": "FALLBACK",
        "description": "Handle general queries or automation tasks that do not match predefined tools.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"]
        }
    }]


def classify_task(task_description):
    json_data = {
                    "model": "gpt-4o-mini", 
                    "messages": [
                                    {"role": "system", "content": "You are a function classifier that extracts structured parameters from queries."},
                                    {"role": "user", "content": task_description}
                                ],
                    "tools": [
                                {
                                    "type": "function",
                                    "function": function
                                } for function in function_definitions_llm
                            ],
                    "tool_choice": "auto"
                }
    
    try:
        result = get_tool_completions(json_data)
        return result
    except json.JSONDecodeError:
        return {"code": "UNKNOWN", "filename": None, "targetfile": None}


import os, json, re

from AIProxy import get_completions

# Define the predefined task descriptions
TASKS_Direct = {
    "A1": "Install `uv` (if required) and run `datagen.py` with `${user.email}` as the only argument.",
    "A2": "Format the contents of `/data/format.md` using `prettier@3.4.2`, updating the file in place.",
    "A3": "Count the number of Wednesdays in `/data/dates.txt` and write just the number to `/data/dates-wednesdays.txt`.",
    "A4": "Sort the array of contacts in `/data/contacts.json` by `last_name`, then `first_name`, and write the result to `/data/contacts-sorted.json`.",
    "A5": "Write the first line of the 10 most recent `.log` files in `/data/logs/` to `/data/logs-recent.txt`, most recent first.",
    "A6": "Find all Markdown (`.md`) files in `/data/docs/`, extract the first occurrence of each H1 (`# Heading`), and create an index file `/data/docs/index.json`.",
    "A7": "Extract the sender's email from `/data/email.txt` using an LLM and write just the email address to `/data/email-sender.txt`.",
    "A8": "Extract the credit card number from `/data/credit-card.png` using an LLM and write it without spaces to `/data/credit-card.txt`.",
    "A9": "Identify the most similar pair of comments in `/data/comments.txt` using embeddings and write them to `/data/comments-similar.txt`, one per line.",
    "A10": "Calculate the total sales of 'Gold' ticket types from `/data/ticket-sales.db` and write the number to `/data/ticket-sales-gold.txt`."
}

# Define the predefined task descriptions
TASKS_refined = {
    "A1": "Run `datagen.py` to generate necessary data files.",
    "A2": "Format `/data/format.md` using Prettier.",
    "A3": "Count the number of a specific weekday in `/data/dates.txt` and save the result.",
    "A4": "Sort contacts in `/data/contacts.json` by last name, then first name.",
    "A5": "Extract the first line from the 10 most recent `.log` files in `/data/logs/`.",
    "A6": "Extract H1 headings from Markdown files in `/data/docs/` and create an index.",
    "A7": "Extract the sender's email from `/data/email.txt`.",
    "A8": "Extract the credit card number from `/data/credit-card.png`.",
    "A9": "Find the most similar pair of comments in `/data/comments.txt`.",
    "A10": "Calculate the total sales of 'Gold' ticket types from `/data/ticket-sales.db`."
}

TASKS_specific = {
    "A1": {"description": "Run `datagen.py` to generate necessary data files.", "filename": None, "targetfile": None},
    "A2": {"description": "Format a markdown file using Prettier.", "filename": "/data/format.md", "targetfile": "/data/format.md"},
    "A3": {"description": "Count the number of Wednesdays in a date file.", "filename": "/data/dates.txt", "targetfile": "/data/dates-wednesdays.txt"},
    "A4": {"description": "Sort contacts in a JSON file.", "filename": "/data/contacts.json", "targetfile": "/data/contacts-sorted.json"},
    "A5": {"description": "Extract the first line from the most recent log files.", "filename": "/data/logs/", "targetfile": "/data/logs-recent.txt"},
    "A6": {"description": "Extract H1 headings from Markdown files.", "filename": "/data/docs/", "targetfile": "/data/docs/index.json"},
    "A7": {"description": "Extract the sender's email from an email file.", "filename": "/data/email.txt", "targetfile": "/data/email-sender.txt"},
    "A8": {"description": "Extract a credit card number from an image.", "filename": "/data/credit-card.png", "targetfile": "/data/credit-card.txt"},
    "A9": {"description": "Find the most similar pair of comments.", "filename": "/data/comments.txt", "targetfile": "/data/comments-similar.txt"},
    "A10": {"description": "Calculate total sales of 'Gold' ticket types from a database.", "filename": "/data/ticket-sales.db", "targetfile": "/data/ticket-sales-gold.txt"}
}

TASKS = {
    "A1": {
        "description": "Run a Python script from a given URL, passing an email as the argument.",
        "filename": r"https?://.*\.py",  # Matches any valid URL ending with .py
        "targetfile": r".*/(.*\.py)",  # Extracts the filename from the URL
        "email": r"[\w\.-]+@[\w\.-]+\.\w+"  # Extracts email ID
    },
    "A2": {
        "description": "Format a markdown file using Prettier.",
        "filename": r"/data/.*format.*\.md",
        "targetfile": r"/data/.*format.*\.md"
    },
    "A3": {
        "description": "Count the number of occurrences of a specific weekday in a date file.",
        "filename": r"/data/.*dates.*\.txt",
        "targetfile": r"/data/.*dates.*\-(monday|tuesday|wednesday|thursday|friday|saturday|sunday).*\.txt",
        #"weekday_index": r"[0-6]"  # Only return the index (0=Monday, ..., 6=Sunday)
        "weekday": r"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)"
    },
    "A4": {
        "description": "Sort contacts in a JSON file.",
        "filename": r"/data/.*contacts.*\.json",
        "targetfile": r"/data/.*contacts.*sorted.*\.json",
        "sorting_fields": [
            {"field": r"\w+", "order": "asc"},
            {"field": r"\w+", "order": "desc"}
        ]
    },
    "A5": {
        "description": "Extract the first line from the most recent log files.",
        "filename": r"/data/logs/.*\.log",
        "targetfile": r"/data/.*logs.*recent.*\.txt",
        "limit": r"[0-9]+",  # Number of log files to process
        "order": r"(asc|desc)"  # Most recent first
    },
    "A6": {
        "description": "Extract specific elements from Markdown (.md) files and generate an index mapping filenames to extracted content.",
        "filename": r"/data/docs/",
        "targetfile": r"/data/docs/.*index.*\.json",
        "extract": r"(H1|h1|H2|h2|H3|h3|H4|h4|H5|h5|H6|h6)",  # Specifies that we extract H1 headings
    },
    "A7": {
        "description": "Extract the sender's email from an email file.",
        "filename": r"/data/.*email.*\.txt",
        "targetfile": r"/data/.*email.*sender.*\.txt"
    },
    "A8": {
        "description": "Extract a credit card number from an image.",
        "filename": r"/data/.*credit.*card.*\.(png|jpg|jpeg)",
        "targetfile": r"/data/.*credit.*card.*\.txt"
    },
    "A9": {
        "description": "Find the most similar pair of comments.",
        "filename": r"/data/.*comments.*\.txt",
        "targetfile": r"/data/.*comments.*similar.*\.txt"
    },
    "A10": {
        "description": "Compute total sales for a specific ticket type in an SQLite database.",
        "filename": r"/data/\w+\.db",
        "targetfile": r"/data/\w+\.txt",
        "table": r"\w+",
        "columns": [r"\w+"],
        "filter": [{
            "column": r"\w+",
            "value": r"\w+"
        }],
        "operation": r"\w+"
    },
    "B3": {
        "description": "Fetch data from an API and save it to a specified file.",
        "filename": r"https?://[^\s]+",  # Matches any API URL starting with http or https
        "targetfile": r"/[\w\-/]+(?:\.\w+)?"  # Matches a valid file path
    },
    "B4": {
        "description": "Clone a Git repository and make a commit.",
        "filename": r"https?://[\w./-]+\.git",  # Matches any Git repository URL
        "targetfile": ""
    },
    "B5": {
        "description": "Run a SQL query on a SQLite or DuckDB database and write the result to a target file.",
        "filename": r"/[\w\-/]+\.db|/[\w\-/]+\.duckdb",  # Matches SQLite (.db) or DuckDB (.duckdb) file
        "targetfile": r"/[\w\-/]+\.\w+",  # Captures any valid target file with an extension
        "query": r".+",  # Captures any SQL query
    },
    "B7": {
        "description": "Compress or resize an image and save it to output_path.",
        "filename": r"/[\w\-/]+\.(jpg|jpeg|png|webp)",  # Matches image files
        "targetfile": r"/[\w\-/]+\.(jpg|jpeg|png|webp)",  # Matches output image files
        "resize_width": r"\d+",  # Extracts width if provided
        "resize_height": r"\d+",  # Extracts height if provided
        "quality": r"\d+",  # Extracts compression quality (1-100)
    },
    "B9": {
        "description": "Convert a Markdown (.md) file to an HTML (.html) file.",
        "filename": r"/[\w\-/]+\.md",  # Matches Markdown files
        "targetfile": r"/[\w\-/]+\.html"  # Matches HTML output files
    }

}


def classify_task(task_description):
    """
    Calls OpenAI API to classify a given task description into a predefined task code.
    Returns a dictionary {code: <task_code>, filename: <file_path>, targetfile: <output_file>}
    """
    prompt = f"""
    You are an automation assistant that maps task descriptions to predefined task codes.
    Your goal is to identify the most relevant predefined task based on the user's input.

    ### Predefined Tasks:
    {chr(10).join([f"{code}: {desc['description']} (filename: {desc['filename']}, targetfile: {desc['targetfile']})" for code, desc in TASKS.items()])}

    ### Instructions:
    - The user's input may be short, paraphrased, or in different languages.
    - Identify the correct task category (`code`).
    - If the task involves specific input and output files, extract them from the description.
    - If no relevant match is found, return `UNKNOWN`.

    ### Expected JSON Output:
    Return a JSON object with `code` as the task code, `filename` as the input file path, and `targetfile` as the output file path.

    ### Examples:

    **User Input:** "input: Install uv (if required) and run https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py with $user.email as the only argument. "
    **Output:** {{"code": "A1", "filename": "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py", "targetfile": "datagen.py", "email": $user.email}}

    **User Input:** "The file /data/dates.txt contains a list of dates, one per line. Count the number of Wednesdays in the list, and write just the number to /data/dates-wednesdays.txt"
    **Output:** {{"code": "A3", "filename": "/data/dates.txt", "targetfile": "/data/dates-wednesdays.txt", "weekday": "Wednesday"}}
    
    **User Input:** "Sort the array of contacts in /data/contacts.json by last_name, then first_name, and write the result to /data/contacts-sorted.json"
	**Output:** {{"code": "A4", "filename": "/data/contacts.json", "targetfile": "/data/contacts-sorted.json", 
	"sorting_fields": ["last_name", "first_name"]}}
 
    **User Input:** "Write the first line of the 10 most recent .log file in /data/logs/ to /data/logs-recent.txt, most recent first"
    **Output:** {{"code": "A5", "filename": "/data/logs/", "targetfile": "/data/logs-recent.txt", "limit": 10, "order": "desc"}}
    
    **User Input:** "Find all Markdown (.md) files in /data/docs/. For each file, extract the first occurrance of each H3 (i.e. a line starting with # ). Create an index file /data/docs/index.json that maps each filename (without the /data/docs/ prefix) "
    **Output:** {{"code": "A6", "filename": "/data/docs/", "targetfile": "/data/docs/index.json", "extract": "H3"}}

    **User Input:** "The SQLite database file /data/ticket-sales.db has a tickets with columns type, units, and price. Each row is a customer bid for a concert ticket. What is the total sales of all the items in the “Gold” ticket type? Write the number in /data/ticket-sales-gold.txt"
    **Output:** {{"code": "A10", "filename": "/data/ticket-sales.db", "targetfile": "/data/ticket-sales-gold.txt", "table": "ticket", "columns": ["type", "units", "price"], "filter": [{{"column": "type", "value": "Gold"}}], "operation": "SUM(units * price)"}}

    **User Input:** "{task_description}"
    **Output:**"""
    
    try:
        result = get_completions([{"role": "system", "content": "You are a helpful assistant"},
                  {"role": "user", "content": prompt}])
        
        #print(result)
        return result
    except json.JSONDecodeError:
        return {"code": "UNKNOWN", "filename": None, "targetfile": None}


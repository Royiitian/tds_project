import os
import json

def execute_task(filename: str, targetfile: str, extract: str) -> str:
    print(f"filename: {filename}, targetfile: {targetfile}, extracttype: {extract}")
    return extract_headings(filename, targetfile, extract)

def extract_headings(foldername, targetfile, extracttype="h1"):
    """
    Extracts the first occurrence of the specified heading type (H1 or H2) in Markdown files from foldername
    and writes an index to targetfile.
    
    :param foldername: Folder containing Markdown files
    :param targetfile: JSON output file path
    :param extracttype: Type of heading to extract ("h1" or "h2")
    """
    valid_headings = {"h1": "# ", "h2": "## ", "h3": "### ", "h4": "#### ", "h5": "##### ", "h6": "###### "}
    
    if extracttype.lower() not in valid_headings:
        print(f"Invalid extract type: {extracttype}. Please choose from: {', '.join(valid_headings.keys())}")
        return

    heading_prefix = valid_headings[extracttype.lower()]
    index = {}

    for root, _, files in os.walk(foldername):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, foldername)  # Keep relative paths in the index

                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith(heading_prefix):  # First H1 or H2 found
                            index[relative_path] = line[len(heading_prefix):].strip()
                            break

    with open(targetfile, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=4)

    print(f"Index file written to {targetfile}")
    return f"Index file written to {targetfile}"
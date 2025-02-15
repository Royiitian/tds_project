import os

from fastapi import HTTPException

def is_valid_path(filepath, base_dir="/data"):
    """Check if a file is inside the /data directory."""
    abs_filepath = os.path.abspath(filepath)
    abs_base_dir = os.path.abspath(base_dir)
    if not abs_filepath.startswith(abs_base_dir):
        raise HTTPException(status_code=403, detail=f"Access to this file: {filepath} is forbidden")
    else:
        return True
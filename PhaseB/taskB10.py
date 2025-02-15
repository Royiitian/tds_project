from fastapi import HTTPException
import pandas as pd
import json

def filter_csv(CSV_FILE_PATH: str, targetfile: str, column: str, value: str):
    print(f"CSV_FILE_PATH: {CSV_FILE_PATH}, targetfile: {targetfile}, column: {column}, value: {value}")
    if not CSV_FILE_PATH or not CSV_FILE_PATH.endswith(".csv") or not column or not value:
        raise HTTPException(status_code=400, detail=f"Input file ({CSV_FILE_PATH}) must be a CSV file and column and value must be provided")
    
    """
    API endpoint to filter a CSV file based on a column and value.

    Query Parameters:
    - column: The column name to filter.
    - value: The value to match in the specified column.

    Returns:
    - JSON data with matching rows.
    """
    try:
        # Load CSV
        df = pd.read_csv(CSV_FILE_PATH)

        # Check if column exists
        if column not in df.columns:
            return {"error": f"Column '{column}' not found in CSV file"}

        # Filter data
        filtered_df = df[df[column].astype(str) == value]

        # Convert to JSON
        result = filtered_df.to_dict(orient="records")
        # save the result to a json file
        if targetfile:
            filtered_df.to_json(targetfile, orient="records", indent=4)
            return targetfile
        else:
            return json.loads(json.dumps(result))  # Convert NumPy types to JSON serializable format

    except Exception as e:
        return {"error": str(e)}
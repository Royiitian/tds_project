import sqlite3
import duckdb
import os
import pandas as pd

def run_sql_query(db_path, targetfile, query):
    print(f"Running SQL query: {query}, {db_path}, {targetfile}")
    """
    Runs a SQL query on a SQLite or DuckDB database and saves the result.
    
    Parameters:
        db_path (str): Path to the SQLite (.db) or DuckDB (.duckdb) database file.
        query (str): SQL query to execute.
        output_file (str): File to save the results.
        output_format (str): "csv" or "json" (default: "csv").
    """
    # Determine database type (SQLite or DuckDB)
    is_duckdb = db_path.endswith(".duckdb")
    
    if not targetfile:
        targetfile = "./data/output_B5.csv"
    elif targetfile.startswith("/"):
        targetfile = f".{targetfile}"
    
    output_format = "csv" if targetfile.endswith(".csv") else "json" if targetfile.endswith(".json") else "txt"

    # Connect to the database
    conn = duckdb.connect(db_path) if is_duckdb else sqlite3.connect(db_path)
    
    try:
        # Execute the query and fetch results into a DataFrame
        df = pd.read_sql_query(query, conn)

        # Save results
        if output_format == "json":
            df.to_json(targetfile, orient="records", indent=4)
        elif output_format == "txt":
            df.to_csv(targetfile, sep="\t", index=False)
        else:  # Default is CSV
            df.to_csv(targetfile, index=False)

        print(f"✅ Query executed successfully. Results saved to {targetfile}")
        
        return targetfile
    except Exception as e:
        print(f"❌ Error executing query: {e}")
    finally:
        conn.close()
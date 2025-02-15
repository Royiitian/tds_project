import sqlite3

def execute_task(filename, targetfile, expression):
    print(f"db_file: {filename}, output_file: {targetfile}, expression: {expression}")

    # Connect to the database and execute query
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        
        # Execute query with filter values
        cursor.execute(expression)
        result = cursor.fetchone()

        # Extract total sales value
        total_sales = result[0] if result and result[0] is not None else 0

        # Write result to file
        with open(targetfile, "w", encoding="utf-8") as f:
            f.write(str(total_sales) + "\n")

        print(f"Total sales for 'Gold' tickets: {total_sales}")
        return f"Total sales for 'Gold' tickets: {total_sales}"
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        if conn:
            conn.close()
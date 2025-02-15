
import os
import glob


def execute_task(filename: str, targetfile: str, num_files, num_lines = 1, order: str="desc") -> str:
    #filename = f"./{filename[3:]}" if filename.startswith(".//") else filename
    print(f"filename: {filename}, targetfile: {targetfile}, numoffiles: {num_files}, num_lines: {num_lines}, order: {order}")
    return write_recent_logs(filename, targetfile, int(num_files), int(num_lines), order)
    

def write_recent_logs(log_dir: str = "./data/logs/", output_file: str = "./data/logs-recent.txt", numoffiles: int = 10, num_lines = 1, order: str = "desc") -> str:
    # Get list of .log files sorted by modification time (most recent first)
    log_files = sorted(
        glob.glob(os.path.join(log_dir, "*.log")),
        key=os.path.getmtime,
        reverse= (order.lower() == "desc")
    )[:numoffiles]  # Get the 10 most recent files

    recent_lines = []

    for log_file in log_files:
        print(f"Reading {num_lines} lines from {log_file}")
        try:
            with open(log_file, "r") as f:
                for _ in range(num_lines):
                    line = f.readline()
                    if not line:  # Stop if EOF is reached
                        break
                    recent_lines.append(line)
        except Exception as e:
            print(f"Error reading {log_file}: {e}")

    # Write to output file
    with open(output_file, "w") as f:
        f.write("".join(recent_lines))

    print(f"Written first lines of {len(recent_lines)} recent logs to {output_file}")
    return f"Written first lines of {len(recent_lines)} recent logs to {output_file}"

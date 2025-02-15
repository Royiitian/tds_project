from datetime import datetime
from dateutil.parser import parse

def execute_task(filename: str, targetfile: str, weekday: int) -> str:
    #weekday_index = weekday_to_number(weekday)
    print(f"🚀 Counting occurrences of weekday {weekday} in {filename}...")
    weekday_count = count_weekday(filename, weekday)

    with open(targetfile, "w", encoding="utf-8") as file:
        file.write(str(weekday_count))

    print(f"✅ Counted {weekday_count} occurrences of weekday {weekday} and wrote to {targetfile}")
    return weekday_count

def count_weekday(file_path, weekday):
    """
    Count the number of occurrences of a specific weekday in a date file.

    :param file_path: Path to the file containing dates (one per line, format: YYYY-MM-DD).
    :param weekday: Target weekday (0=Monday, 1=Tuesday, ..., 6=Sunday).
    :return: Count of the specified weekday.
    """
    count = 0
    expected = 0
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            date_str = line.strip()
            try:
                if parse(date_str).weekday() == weekday:
                    expected += 1
            except ValueError:
                continue
            # Try different formats to parse the date correctly
            for fmt in ("%Y/%m/%d %H:%M:%S", "%Y-%m-%d", "%b %d, %Y", "%d-%b-%Y", "%Y/%m/%d"):
                try:
                    date_obj = datetime.strptime(date_str, fmt)
                    if date_obj.weekday() == weekday:
                        #print(f"{date_obj}| {date_str}          | {fmt}         | {date_obj.weekday()}")
                        count += 1
                    break
                except ValueError:
                    continue
    print(f"🚀🚀 Expected: {expected} 🚀🚀")
    return count
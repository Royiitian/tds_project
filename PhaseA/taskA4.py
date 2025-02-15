import json

def execute_task(filename: str, targetfile: str, sorting_fields) -> str:
    print(f"filename: {filename}, targetfile: {targetfile}, sorting_fields: {sorting_fields}")
    return sort_contacts(filename, targetfile, sorting_fields)

def sort_contacts(input_file, output_file, sorting_fields):
    # Load contacts from JSON
    with open(input_file, "r") as f:
        contacts = json.load(f)
        
    # Sort using the provided sort fields
    contacts_sorted = sorted(contacts, key=lambda c: [c[field].lower() for field in sorting_fields if field in c])

    # Write sorted contacts to output file
    with open(output_file, "w") as f:
        json.dump(contacts_sorted, f, indent=2)

    print(f"Sorted contacts saved to {output_file}")
    return f"Task A4: Sorted contacts saved to {output_file}"



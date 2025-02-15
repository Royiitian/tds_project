import requests, json



def fetch_and_save_data(filename, targetfile):
    try:
        # Make the API request
        response = requests.get(filename)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

        # Parse JSON response
        data = response.json()

        # Save the data to a file
        with open(targetfile, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print(f"Data successfully saved to {targetfile}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
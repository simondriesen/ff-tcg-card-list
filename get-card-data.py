import os
import csv
import json
import requests
from datetime import datetime

URL = "http://www.square-enix-shop.com/jp/ff-tcg/card/data/list_card.txt"

# Fetch data from the API
try:
    response = requests.get(URL)
    response.raise_for_status()  # Raise an error for bad status codes
    api_data = response.text  # Get the response content as text
except requests.exceptions.RequestException as e:
    print(f"Error fetching API data: {e}")
    api_data = ""

# Check if API data was successfully fetched
if api_data:
    # Append the API response to a file
    timestamp = datetime.now().strftime('%Y-%m-%d')
    csv_file = f"card-data_{timestamp}.csv"
    folder_path = "raw-data"
    os.makedirs(folder_path, exist_ok=True)
    csv_file_path = os.path.join(folder_path, csv_file)
    
    try:
        with open(csv_file_path, "w", encoding='utf-8') as file:
            file.write(api_data)
    except IOError as e:
        print(f"Error writing CSV file: {e}")
        exit()

    # Define the column names for the CSV file
    fieldnames = [
        "Code", "Symbol", "Japanese Text", "Number", "Game Title",
        "Original Title", "Additional Info", "Image File", "Link", "Copyright"
    ]

    # Read the CSV file
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            # Assuming the data is tab-separated
            csv_reader = csv.DictReader(file, fieldnames=fieldnames, delimiter='\t')

            data = []
            for row in csv_reader:
                # Clean up any row that has unexpected fields
                if any(value is not None and value != '' for value in row.values()):
                    data.append(row)

    except IOError as e:
        print(f"Error reading CSV file: {e}")
        exit()

    # Write the data to a JSON file
    json_file = f"card-data_{timestamp}.json"
    json_file_path = os.path.join(folder_path, json_file)
    
    try:
        with open(json_file_path, mode='w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Error writing JSON file: {e}")
        exit()

    print(f"Files created successfully: {csv_file_path}, {json_file_path}")
else:
    print("No data fetched from the API.")
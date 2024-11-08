import os
import csv
import json
import requests
from collections import defaultdict

# Fetch data from the JP API
JP_URL = "http://www.square-enix-shop.com/jp/ff-tcg/card/data/list_card.txt"

try:
    response = requests.get(JP_URL)
    response.raise_for_status()
    api_data = response.text
except requests.exceptions.RequestException as e:
    print(f"Error fetching API data: {e}")
    api_data = ""

# Check if API data was successfully fetched
if api_data:
    os.makedirs("files", exist_ok=True)
    csv_file = os.path.join("files", "cards.jp.csv")
    
    try:
        with open(csv_file, "w", encoding='latin1') as file:
            file.write(api_data)
    except IOError as e:
        print(f"Error writing CSV file: {e}")
        exit()

    # Define the column names for the CSV file
    fieldnames = [
        "code", "element_jp", "name_jp", "expansion_number", "image_source", "original_title", 
        "category", "image_file", "promo_info", "starter_info", "filter_link", "copyright"
    ]

    # Read the CSV file
    data = []
    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file, delimiter='\t')

            # Process each row and map to fieldnames
            for row in csv_reader:
                if len(row) >= len(fieldnames):  # Ensure there are enough columns
                    entry = {fieldnames[i]: row[i] for i in range(len(fieldnames))}
                    data.append(entry)

    except IOError as e:
        print(f"Error reading CSV file: {e}")
        exit()

    # Write the data to a JSON file
    json_file = os.path.join("files", "cards.jp.json")
    combined = defaultdict(dict)
    
    try:
        for item in data:
            card_code = item.get("code")

            # Split lines in 'copyright' if it exists
            if 'copyright' in item and item['copyright']:
                item['copyright'] = [line.strip() for line in item['copyright'].split("\n")]

            # Initialize combined[obj_id] if it's the first occurrence
            if card_code not in combined:
                combined[card_code] = item.copy()
                combined[card_code]["images"] = [item["image_file"]] if "image_file" in item else []
                combined[card_code].pop("image_file", None)

            else:
                for key, value in item.items():
                    if key == "code":
                        continue

                    # Special handling for "image_file" to always keep it as an array in "images"
                    if key == "image_file":
                        if value not in combined[card_code]["images"]:
                            combined[card_code]["images"].append(value)
                    
                    # Handle all other fields normally
                    elif key not in combined[card_code]:
                        combined[card_code][key] = value

        # Convert the defaultdict back to a list of dictionaries
        combined_data = list(combined.values())

        # Write to JSON file
        with open(json_file, mode='w', encoding='utf-8') as file:
            json.dump(combined_data, file, indent=4, ensure_ascii=False)

    except IOError as e:
        print(f"Error writing JSON file: {e}")
        exit()

    print(f"Files created successfully: {csv_file}, {json_file}")

    # Create the directory to store images, if it doesn't exist
    # if not os.path.exists('images'):
    #     os.makedirs('images')

    # for item in data:
    #     image_url = f"http://www.square-enix-shop.com/jp/ff-tcg/card/cimg/thumb/{item.get('image_file')}"

    #     # Extract the image filename from the URL
    #     image_name = os.path.basename(image_url)
    #     image_path = os.path.join('images', image_name)
        
    #     # Download the image
    #     try:
    #         response = requests.get(image_url)
    #         if response.status_code == 200:
    #             # Save the image to the 'images' directory
    #             with open(image_path, 'wb') as f:
    #                 f.write(response.content)
    #             print(f"Downloaded {image_name}")
    #         else:
    #             print(f"Failed to download {image_name}: Status code {response.status_code}")
    #     except Exception as e:
    #         print(f"Error downloading {image_url}: {e}")
else:
    print("No data fetched from the API (jp).")

# Fetch data from the JP API
EN_URL = "https://fftcg.square-enix-games.com/en/get-cards"

# JSON payload
payload = {
    "text": "",
}

try:
    response = requests.post(EN_URL, json=payload)
    response.raise_for_status()
    api_data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching API data: {e}")
    api_data = ""

# Check if API data was successfully fetched
if api_data:
    os.makedirs("files", exist_ok=True)
    json_file = os.path.join("files", "cards.en.json")

    try:
        with open(json_file, mode='w', encoding='utf-8') as file:
            json.dump(api_data["cards"], file, ensure_ascii=False, indent=4)
        print(f"File created successfully: {json_file}")
    except IOError as e:
        print(f"Error writing JSON file: {e}")
        exit()

else:
    print("No data fetched from the API (en).")
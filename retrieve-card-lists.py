import os
import csv
import json
import requests

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
    combined = {}
    
    try:
        for item in data:
            card_code = item.get("code")

            # Split lines in 'copyright' if it exists
            if 'copyright' in item and item['copyright']:
                item['copyright'] = [line.strip() for line in item['copyright'].split("\n")]

            # Initialize combined[obj_id] if it's the first occurrence
            if card_code not in combined:
                combined[card_code] = item.copy()
                
                # Check if "image_file" exists and convert it to full URL format
                if "image_file" in item:
                    thumb_url = f"http://www.square-enix-shop.com/jp/ff-tcg/card/cimg/thumb/{item['image_file']}"
                    full_url = f"http://www.square-enix-shop.com/jp/ff-tcg/card/cimg/large/{item['image_file']}"

                    # Initialize "images_jp" with full URLs for thumbs and full
                    combined[card_code]["images_jp"] = {
                        "thumbs": [thumb_url],
                        "full": [full_url]
                    }
                    
                    # Remove the original "image_file" key from the item copy
                    combined[card_code].pop("image_file", None)
                else:
                    # Initialize "images_jp" with empty lists if no image file exists
                    combined[card_code]["images_jp"] = {"thumbs": [], "full": []}

            else:
                for key, value in item.items():
                    if key == "code":
                        continue

                    thumb_url = f"http://www.square-enix-shop.com/jp/ff-tcg/card/cimg/thumb/{value}"
                    full_url = f"http://www.square-enix-shop.com/jp/ff-tcg/card/cimg/large/{value}"

                    # Add url to both "thumbs" and "full"
                    if key == "image_file":
                        # Append to "thumbs" array if not already present
                        if thumb_url not in combined[card_code]["images_jp"]["thumbs"]:
                            combined[card_code]["images_jp"]["thumbs"].append(thumb_url)

                        # Append to "full" array if not already present
                        if full_url not in combined[card_code]["images_jp"]["full"]:
                            combined[card_code]["images_jp"]["full"].append(full_url)

        # Write to JSON file
        with open(json_file, mode='w', encoding='utf-8') as file:
            json.dump(combined, file, indent=4, ensure_ascii=False)

    except IOError as e:
        print(f"Error writing JSON file: {e}")
        exit()

    print(f"Files created successfully: {csv_file}, {json_file}")

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
    keys_to_remove = [
        "name_de", "type_de", "job_de", "text_de",
        "name_es", "type_es", "job_es", "text_es",
        "name_fr", "type_fr", "job_fr", "text_fr",
        "name_it", "type_it", "job_it", "text_it"
    ]

    try:
        # Modify each card in the "cards" array
        if isinstance(api_data.get("cards"), list):
            for card in api_data["cards"]:
                if isinstance(card, dict):
                    # Remove specified keys
                    for key in keys_to_remove:
                        card.pop(key, None)
                    # Rename "images" to "images_en"
                    if "images" in card:
                        card["images_en"] = card.pop("images")
        
        # Write to JSON file    
        with open(json_file, mode='w', encoding='utf-8') as file:
            json.dump(api_data["cards"], file, ensure_ascii=False, indent=4)
        print(f"File created successfully: {json_file}")
    
    except IOError as e:
        print(f"Error writing JSON file: {e}")
        exit()

else:
    print("No data fetched from the API (en).")
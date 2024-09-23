import csv
import json
import requests

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
    csv_file = f"cards.csv"
    
    try:
        with open(csv_file, "w", encoding='latin1') as file:
            file.write(api_data)
    except IOError as e:
        print(f"Error writing CSV file: {e}")
        exit()

    # Define the column names for the CSV file
    fieldnames = [
        "code", "type_jp", "text_jp", "expansion_number", "image_source", "original_title", 
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
    json_file = f"cards.json"
    
    try:
        for item in data:
            if 'copyright' in item and item['copyright']:
                item['copyright'] = [line.strip() for line in item['copyright'].split("\n")]
        with open(json_file, mode='w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Error writing JSON file: {e}")
        exit()

    print(f"Files created successfully: {csv_file}, {json_file}")

    try:
        for item in data:
            image_url = f"http://www.square-enix-shop.com/jp/ff-tcg/card/cimg/thumb/{item.get('image_file')}"

            # Extract the image filename from the URL
            image_name = os.path.basename(image_url)
            image_path = os.path.join('images', image_name)
            
            # Download the image
            try:
                response = requests.get(image_url)
                if response.status_code == 200:
                    # Save the image to the 'images' directory
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Downloaded {image_name}")
                else:
                    print(f"Failed to download {image_name}: Status code {response.status_code}")
            except Exception as e:
                print(f"Error downloading {image_url}: {e}")
else:
    print("No data fetched from the API.")
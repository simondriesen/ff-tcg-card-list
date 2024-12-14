import os
import json
import requests

# Open and load the cards.jp.json file
with open('files/cards.jp.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Iterate over the array of cards
for card in data:
    for image_url in card['images_jp']['full']:
        image_name = os.path.basename(image_url)
        image_path = os.path.join('images', image_name)
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded {image_name}")
            else:
                print(f"Failed to download {image_name}: Status code {response.status_code}")
        except Exception as e:
            print(f"Error downloading {image_url}: {e}")
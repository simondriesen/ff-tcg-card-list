import os
import json
import requests
from io import BytesIO
from PIL import Image

# Open and load the cards.jp.json file
with open('files/cards.jp.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Iterate over the array of cards
for card in data:
    for image_url in card['images_jp']['full']:
        png_file = os.path.basename(image_url)
        webp_file = os.path.splitext(png_file)[0] + ".webp"
        set_code = png_file.split('-')[0]
        image_path = os.path.join('images', 'jp', set_code, webp_file)
        
        if os.path.exists(image_path):
            print(f"{webp_file} already exists. Skipping.")
            continue

        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                try:
                    # Open the image from the response content (as a PNG)
                    img = Image.open(BytesIO(response.content))
                    
                    # Save the image as WebP
                    img.save(image_path, "WEBP", lossless=True)
                    print(f"Image saved as WebP: {image_path}")
                except Exception as e:
                    print(f"Error converting image: {e}")
            else:
                print(f"Failed to download {png_file}: Status code {response.status_code}")

        except Exception as e:
            print(f"Error downloading {image_url}: {e}")
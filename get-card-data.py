import requests
import os
from datetime import datetime

# API URL
API_URL = "http://www.square-enix-shop.com/jp/ff-tcg/card/data/list_card.txt"

# Fetch data from the API
try:
    response = requests.get(API_URL)
    response.raise_for_status()  # Raise an error for bad status codes
    api_data = response.text  # Get the response content as text
except requests.exceptions.RequestException as e:
    print(f"Error fetching API data: {e}")
    api_data = f"Error fetching API data: {e}"

# Append the API response to a file
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
filename = f"card_data_{timestamp}.txt"
file_path = os.path.join("raw-data", filename)
with open(filename, "a") as file:
    file.write(api_data)

print(f"File created succesfully.")

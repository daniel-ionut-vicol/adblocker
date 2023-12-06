import os
import json
import requests

# Directory to store the downloaded images
download_dir = "ad"

# Create the download directory if it doesn't exist
os.makedirs(download_dir, exist_ok=True)

# Load the list of image filenames from the JSON file
with open("images.json", "r") as json_file:
    image_filenames = json.load(json_file)

# Function to download an image and keep track of downloaded images in a subfolder
def download_image(image_url, subfolder):
    filename = os.path.join(download_dir, subfolder, os.path.basename(image_url))
    if not os.path.exists(filename):
        response = requests.get(image_url)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "wb") as file:
                file.write(response.content)
                print(f"Downloaded: {filename}")
                # Create a record of downloaded images in the subfolder
                with open(os.path.join(download_dir, subfolder, "downloaded_images.txt"), "a") as record_file:
                    record_file.write(os.path.basename(image_url) + "\n")
        else:
            print(f"Failed to download: {image_url}")

# Loop through the subfolders and download images
for subfolder in range(3):  # Replace 3 with the number of subfolders you want to iterate through
    base_url = f"https://people.cs.pitt.edu/~mzhang/image_ads/{subfolder}/"
    
    # Load the list of already downloaded images in this subfolder
    downloaded_images = set()
    record_file_path = os.path.join(download_dir, str(subfolder), "downloaded_images.txt")
    if os.path.exists(record_file_path):
        with open(record_file_path, "r") as record_file:
            downloaded_images = set(record_file.read().splitlines())
    
    for filename in image_filenames:
        if os.path.basename(filename) not in downloaded_images:
            image_url = base_url + filename
            download_image(image_url, str(subfolder))

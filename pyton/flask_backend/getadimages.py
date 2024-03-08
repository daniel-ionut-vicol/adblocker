import os
import requests
from bs4 import BeautifulSoup
import concurrent.futures

# Base URL of the directory of images
base_url = "https://people.cs.pitt.edu/~mzhang/image_ads/"

# Directory to store the downloaded images
download_dir = "ad"

# Function to download an image
def download_image(image_url):
    filename = os.path.join(download_dir, image_url.replace(base_url, ''))
    if not os.path.exists(filename):
        try:
            response = requests.get(image_url, timeout=60)
            response.raise_for_status()
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"Downloaded: {filename}")
        except (requests.exceptions.RequestException, IOError) as e:
            print(f"Failed to download: {image_url}. Error: {e}")

# Function to traverse each folder and subfolder and download all images
def traverse_and_download(url):
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        images = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href.endswith('/'):
                traverse_and_download(url + href)
            elif href.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                images.append(url + href)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(download_image, images)
    except (requests.exceptions.RequestException, IOError) as e:
        print(f"Failed to traverse: {url}. Error: {e}")

# Start the process
traverse_and_download(base_url)

import os
import json
import aiohttp
import asyncio
import logging
from aiohttp import ClientSession
from tqdm.asyncio import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Directory to store the downloaded images
download_dir = "ad"
os.makedirs(download_dir, exist_ok=True)

# Load the list of image filenames from the JSON file
with open("images.json", "r") as json_file:
    image_filenames = json.load(json_file)

# Async function to check if the link is valid
async def is_link_valid(session, url, url_cache):
    if url in url_cache:
        return url_cache[url]

    try:
        async with session.head(url) as response:
            is_valid = response.status == 200
            url_cache[url] = is_valid
            return is_valid
    except Exception as e:
        logging.error(f"Error checking link {url}: {e}")
        return False

# Async function to download an image
async def download_image(session, image_url, subfolder, url_cache):
    if await is_link_valid(session, image_url, url_cache):
        filename = os.path.join(download_dir, subfolder, os.path.basename(image_url))
        if not os.path.exists(filename):
            try:
                async with session.get(image_url) as response:
                    if response.status == 200:
                        with open(filename, "wb") as file:
                            while True:
                                chunk = await response.content.read(1024)
                                if not chunk:
                                    break
                                file.write(chunk)
                        logging.info(f"Downloaded: {filename}")
                        return os.path.basename(image_url)
            except Exception as e:
                logging.error(f"Error downloading {image_url}: {e}")
    return None

# Async function to process each subfolder
async def process_subfolder(session, subfolder, image_filenames):
    logging.info(f"Processing subfolder: {subfolder}")
    base_url = f"https://people.cs.pitt.edu/~mzhang/image_ads/{subfolder}/"
    record_file_path = os.path.join(download_dir, str(subfolder), "downloaded_images.txt")

    if os.path.exists(record_file_path):
        with open(record_file_path, "r") as record_file:
            downloaded_images = set(record_file.read().splitlines())
    else:
        downloaded_images = set()
        os.makedirs(os.path.dirname(record_file_path), exist_ok=True)

    url_cache = {}
    tasks = [download_image(session, base_url + filename, str(subfolder), url_cache) 
             for filename in image_filenames if os.path.basename(filename) not in downloaded_images]

    # Create a tqdm progress bar for the tasks
    downloaded_files = []
    async for result in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        downloaded_files.append(await result)

    with open(record_file_path, "a") as record_file:
        for downloaded_file in downloaded_files:
            if downloaded_file:
                record_file.write(downloaded_file + "\n")

# Main async execution function
async def main():
    async with ClientSession() as session:
        for subfolder in range(3): # Adjust as needed
            await process_subfolder(session, str(subfolder), image_filenames)

# Run the main function
asyncio.run(main())


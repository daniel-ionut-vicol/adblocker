import os
from PIL import Image

def is_image_corrupt(image_path):
    try:
        with Image.open(image_path) as img:
            img.verify()  # Verify if it's an image
        return False
    except Exception:
        return True

# Function to recursively collect all image file paths in a given directory
def collect_image_paths(root_dir, label, image_limit):
    file_paths = []
    labels = []
    corrupt_images_log = "corrupt_images.log"
    
    print(f"Scanning in directory: {root_dir}")  # Debugging print
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if image_limit != "all" and len(file_paths) >= int(image_limit):
                break

            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(subdir, file)

                if is_image_corrupt(file_path):
                    with open(corrupt_images_log, "a") as log:
                        log.write(file_path + "\n")
                    continue

                file_paths.append(file_path)
                labels.append(label)

    if not file_paths:
        print("No images found. Check the directory path and file extensions.")  # Debugging print
    else:
        print(f"{len(file_paths)} images for label={label}")
    return file_paths, labels

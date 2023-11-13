from PIL import Image

def is_image_corrupt(image_path):
    try:
        with Image.open(image_path) as img:
            img.verify()  # Verify if it's an image
        return False
    except Exception:
        return True

# Function to read input with default value
def get_input(prompt, default=None):
    user_input = input(f"{prompt}({default}): ")
    return user_input if user_input else default
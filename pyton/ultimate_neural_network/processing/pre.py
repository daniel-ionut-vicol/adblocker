import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Function to load and preprocess a single image
def preprocess_image(image_path, target_size):
    img = load_img(image_path, target_size=target_size)
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    return img

def pre_resnet50(image_path, target_size):
    try:
        img = load_img(image_path, target_size=target_size)
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0)
        return tf.keras.applications.resnet50.preprocess_input(img)
    except IOError:
        print(f"Warning: Skipping corrupted/truncated image: {image_path}")
        return None  # or an alternative handling method
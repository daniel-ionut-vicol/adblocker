import sys
sys.path.append("..")

import numpy as np
from processing.pre import preprocess_image
import config

def custom_generator(
    file_paths, labels, batch_size, target_size, processor, text_prompts
):
    num_samples = len(file_paths)
    while True:
        for offset in range(0, num_samples, batch_size):
            batch_paths = file_paths[offset : offset + batch_size]
            batch_labels = labels[offset : offset + batch_size]

            images = [preprocess_image(path, target_size) for path in batch_paths]
            images = np.vstack(images)

            # Map each image to its corresponding text prompt
            batch_texts = [text_prompts[label] for label in batch_labels]

            # Process text inputs
            text_inputs = processor(
                text=batch_texts,
                max_length=config.TEXT_INPUT_SIZE,
                padding="max_length",
                truncation=True,
                return_tensors="tf",
            ).input_ids

            yield {"image_input": images, "text_input": text_inputs}, np.array(
                batch_labels
            )

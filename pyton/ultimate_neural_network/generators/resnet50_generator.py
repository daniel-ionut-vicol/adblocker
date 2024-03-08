import sys
sys.path.append("..")

from processing.pre import pre_resnet50
import numpy as np

# Custom generator
def custom_generator(file_paths, labels, batch_size, target_size):
    batch_size = int(batch_size)
    num_samples = len(file_paths)
    target_size = (int(target_size[0]), int(target_size[1]))
    while True:
        for offset in range(0, num_samples, batch_size):
            batch_paths = file_paths[offset:offset + batch_size]
            batch_labels = labels[offset:offset + batch_size]

            images = [pre_resnet50(path, target_size) for path in batch_paths]
            images = [img for img in images if img is not None]  # Exclude None values
            if not images:  # Skip batch if all images were corrupted
                continue

            images = np.vstack(images)
            yield images, np.array(batch_labels)
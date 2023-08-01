import os
import tensorflow as tf

class DataSetLoader:
    image_extensions = ['.jpg', '.jpeg', '.png']   
    
    def __init__(self) -> None:
        pass

    def count_images(self, path):
        image_count = 0
        for filename in os.listdir(path):
            if any(filename.endswith(ext) for ext in self.image_extensions):
                image_count += 1
        return image_count

    def get_dataset(self, path, label):
        print(f"Getting images from {path}")
        return tf.keras.preprocessing.image_dataset_from_directory(
            path,
            image_size=(256, 256),
            batch_size=32,
            labels=[int(label)] * self.count_images(path),
            label_mode="int",
        )

    def load(self, path, label=None):
        datasets = []
        for directory in os.listdir(path):
            new_path = os.path.join(path, directory)
            if os.path.isdir(new_path):
                datasets.append(self.load(new_path, label))
            else:
                datasets.append(self.get_dataset(path, label))
                break

        final_dataset = datasets[0]
        for dataset in datasets[1:]:
            final_dataset = final_dataset.concatenate(dataset)

        return final_dataset

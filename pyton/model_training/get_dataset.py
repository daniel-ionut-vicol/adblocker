import os
import tensorflow as tf

class DataSetLoader:    
    def __init__(self) -> None:
        pass

    def collect_images(self, directory, label_map):
        file_paths = []
        labels = []
        for label_dir in os.listdir(directory):
            label_dir_path = os.path.join(directory, label_dir)
            if os.path.isdir(label_dir_path):
                for root, dirs, files in os.walk(label_dir_path):
                    for file in files:
                        if file.endswith(('.jpg', '.jpeg', '.png')):
                            file_path = os.path.join(root, file)
                            label = label_map[label_dir]
                            file_paths.append(file_path)
                            labels.append(label)
        return file_paths, labels
    
    def count_images(self, path):
        image_count = 0
        for filename in os.listdir(path):
            if any(filename.endswith(ext) for ext in self.image_extensions):
                image_count += 1
        return image_count

    def get_dataset(self, path, label):
        return tf.keras.preprocessing.image_dataset_from_directory(
            path,
            image_size=(256, 256),
            batch_size=32,
            labels=[int(label)] * self.count_images(path),
            label_mode="binary",
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

#         final_dataset = datasets[0]
#         for dataset in datasets[1:]:
#             final_dataset = final_dataset.concatenate(dataset)

#         # Calculate the total number of batches
#         num_batches = tf.data.experimental.cardinality(final_dataset).numpy()

#         # Repeat the dataset to create an infinite stream of batches
#         repeated_dataset = final_dataset.repeat()

#         # Take a fixed number of batches from the repeated dataset
#         final_dataset = repeated_dataset.take(num_batches)

#         return final_dataset

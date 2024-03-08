import tensorflow as tf

class ImageDataset:
    def __init__(self, image_paths, image_labels, BATCH_SIZE, image_min_side):
        self.image_paths = image_paths
        self.image_labels = image_labels
        self.BATCH_SIZE = BATCH_SIZE
        self.image_min_side = image_min_side

    def load_and_preprocess_image(self, image_path, label):
        img = tf.io.read_file(image_path)
        img = tf.image.decode_jpeg(img, channels=3)
        img = tf.image.resize(img, [self.image_min_side, self.image_min_side])
        img = img / 255.0  # normalize to [0,1] range
        return img, label

    def create_tf_dataset(self):
        dataset = tf.data.Dataset.from_tensor_slices((self.image_paths, self.image_labels))
        dataset = dataset.map(self.load_and_preprocess_image)
        dataset = dataset.batch(self.BATCH_SIZE)
        return dataset


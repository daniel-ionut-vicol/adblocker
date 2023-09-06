import os
import numpy as np
import cv2
import tensorflow as tf

class Generator(tf.keras.utils.Sequence):

    def __init__(self, image_paths, image_labels, BATCH_SIZE=int(os.environ['BATCH_SIZE']), shuffle_images=True, image_min_side=int(os.environ['IMAGE_SIZE']), is_training=True):
        """ Initialize Generator object.
        Args
            image_paths            : List of image file paths.
            image_labels           : List of image labels.
            BATCH_SIZE             : The size of the batches to generate.
            shuffle_images         : If True, shuffles the images.
            image_min_side         : After resizing the minimum side of an image is equal to image_min_side.
            is_training            : Indicates whether the generator is for training data.
        """
        self.batch_size = BATCH_SIZE
        self.shuffle_images = shuffle_images
        self.image_min_side = image_min_side
        self.is_training = is_training

        # Load image paths and labels
        self.image_paths = image_paths
        self.image_labels = image_labels
        
        self.create_image_groups()
    
    def create_image_groups(self):
        if self.shuffle_images:
            # Randomly shuffle dataset
            seed = 4321
            np.random.seed(seed)
            np.random.shuffle(self.image_paths)
            np.random.seed(seed)
            np.random.shuffle(self.image_labels)

        # Divide image_paths and image_labels into groups of BATCH_SIZE
        self.image_groups = [[self.image_paths[x % len(self.image_paths)] for x in range(i, i + self.batch_size)]
                              for i in range(0, len(self.image_paths), self.batch_size)]
        self.label_groups = [[self.image_labels[x % len(self.image_labels)] for x in range(i, i + self.batch_size)]
                              for i in range(0, len(self.image_labels), self.batch_size)]


    def resize_image(self, img, target_size):
        # Convert the image to a TensorFlow tensor
        img = tf.convert_to_tensor(img, dtype=tf.float32)

        # Resize the image using TensorFlow to the specified size (e.g., 256x256)
        resized_image = tf.image.resize(img, (target_size, target_size))

        return resized_image.numpy()  # Convert back to NumPy array for compatibility
    
    def load_images(self, image_group):
        images = []
        for image_path in image_group:
            img = cv2.imread(image_path)
            img_shape = len(img.shape)
            if img_shape == 2:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            elif img_shape == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
            elif img_shape == 3:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = self.resize_image(img, self.image_min_side)

            # Normalize the image
            img = img / 255.0  # Assuming pixel values are in the range [0, 255]

            images.append(img)

        return images

    def construct_image_batch(self, image_group):
        # get the max image shape
        max_shape = tuple(max(image.shape[x] for image in image_group) for x in range(3))

        # construct an image batch object
        image_batch = np.zeros((self.batch_size,) + max_shape, dtype='float32')

        # copy all images to the upper left part of the image batch object
        for image_index, image in enumerate(image_group):
            image_batch[image_index, :image.shape[0], :image.shape[1], :image.shape[2]] = image

        return image_batch
    
    def __len__(self):
        """
        Number of batches for generator.
        """

        return len(self.image_groups)

    def __getitem__(self, index):
        """
        Keras sequence method for generating batches.
        """
        image_group = self.image_groups[index]
        label_group = self.label_groups[index]
        images = self.load_images(image_group)
        image_batch = self.construct_image_batch(images)

        return np.array(image_batch), np.array(label_group)
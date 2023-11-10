import os
import datetime
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from eval import eval
import config

# Load the pre-trained ResNet50 model without the top layer
base_model = ResNet50(weights='imagenet', include_top=False)

# Freeze the layers of the base model
for layer in base_model.layers:
    layer.trainable = False

# Add new layers for binary classification
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(1, activation='sigmoid')(x)  # Single output node for binary classification

model = Model(inputs=base_model.input, outputs=predictions)


# Compile the model with binary cross-entropy loss
model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

# Function to load and preprocess a single image
def preprocess_image(image_path, target_size):
    img = load_img(image_path, target_size=target_size)
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    return tf.keras.applications.resnet50.preprocess_input(img)

# Custom generator
def custom_generator(file_paths, labels, batch_size, target_size):
    num_samples = len(file_paths)
    while True:  # Loop forever so the generator never terminates
        for offset in range(0, num_samples, batch_size):
            batch_paths = file_paths[offset:offset + batch_size]
            batch_labels = labels[offset:offset + batch_size]

            images = [preprocess_image(path, target_size) for path in batch_paths]
            images = np.vstack(images)
            
            yield images, np.array(batch_labels)

# Function to recursively collect all image file paths in a given directory
def collect_image_paths(root_dir, label):
    file_paths = []
    labels = []
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):  # Check for image file extensions
                file_path = os.path.join(subdir, file)
                file_paths.append(file_path)
                labels.append(label)
    return file_paths, labels

# Collect image paths and labels
ad_paths, ad_labels = collect_image_paths(os.path.join(config.DATASET_PATH, 'ad'), 0)  # Label for 'Ad'
nonad_paths, nonad_labels = collect_image_paths(os.path.join(config.DATASET_PATH, 'nonAd'), 1)  # Label for 'NonAd'

# Combine the paths and labels
file_paths = ad_paths + nonad_paths
labels = ad_labels + nonad_labels

# Split the data into training and validation sets
train_paths, val_paths, train_labels, val_labels = train_test_split(file_paths, labels, test_size=0.2, random_state=42)

# Split the data into training and validation sets
train_paths, val_paths, train_labels, val_labels = train_test_split(file_paths, labels, test_size=0.2, random_state=42)

train_generator = custom_generator(train_paths, train_labels, config.BATCH_SIZE, (config.IMAGE_SIZE, config.IMAGE_SIZE))
val_generator = custom_generator(val_paths, val_labels, config.BATCH_SIZE, (config.IMAGE_SIZE, config.IMAGE_SIZE))

# Assuming 'model' is your compiled model (e.g., based on ResNet50)
# Define the number of steps per epoch for training and validation
train_steps = len(train_paths) // config.BATCH_SIZE
val_steps = len(val_paths) // config.BATCH_SIZE

start_datetime = datetime.datetime.now()

# Fit the model
history = model.fit(
    train_generator,
    steps_per_epoch=train_steps,
    epochs=config.EPOCHS,  # Number of epochs
    validation_data=val_generator,
    validation_steps=val_steps
)

finish_datetime = datetime.datetime.now()

eval(model, val_generator, history, start_datetime, finish_datetime)
import os
import datetime
import random
import numpy as np
import tensorflow as tf
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import ModelCheckpoint
from PIL import Image
# ---------------
import config
from ultimate_generator import Generator
from resnet50_model import get_model
from eval import eval

def load_image_paths_labels(DATASET_PATH):
    classes = os.listdir(DATASET_PATH)
    lb = preprocessing.LabelBinarizer()
    lb.fit(classes)

    image_paths = []
    image_labels = []

    # Get class names directly from the list of classes
    for class_name in classes:
        class_path = os.path.join(DATASET_PATH, class_name)
        
        if os.path.isdir(class_path):  # Ensure it's a directory
            # Recursively traverse the directory structure
            for root, _, files in os.walk(class_path):
                for image_file_name in files:
                    if image_file_name.endswith(".png"):
                        image_path = os.path.join(root, image_file_name)

                        # Attempt to open the image
                        try:
                            img = Image.open(image_path)
                            img.verify()  # Verify the image file
                        except (IOError, SyntaxError) as e:
                            print(f"Skipping invalid image: {image_path}")
                            continue

                        image_paths.append(image_path)
                        image_labels.append(class_name)

    image_labels = np.array(lb.transform(image_labels), dtype='float32')

    assert len(image_paths) == len(image_labels)

    # Combine the lists into a list of tuples
    combined = list(zip(image_paths, image_labels))
    
    # Shuffle the combined list
    random.shuffle(combined)
    
    # Unzip the shuffled list back into separate lists
    image_paths[:], image_labels[:] = zip(*combined)

    return image_paths, image_labels

# Load image paths and labels
image_paths, image_labels = load_image_paths_labels(config.DATASET_PATH)

# Split the data into training, validation, and test sets
train_paths, temp_paths, train_labels, temp_labels = train_test_split(image_paths, image_labels, test_size=0.2, random_state=42)
val_paths, test_paths, val_labels, test_labels = train_test_split(temp_paths, temp_labels, test_size=0.5, random_state=42)

# Create generators for training, validation, and test sets
train_generator = Generator(train_paths, train_labels, BATCH_SIZE=config.BATCH_SIZE, is_training=True)
val_generator = Generator(val_paths, val_labels, BATCH_SIZE=config.BATCH_SIZE, is_training=False)
test_generator = Generator(test_paths, test_labels, BATCH_SIZE=config.BATCH_SIZE, is_training=False)

# CALLBACKS -----------------------------------
# Define a callback for dynamic checkpoint naming and specific folder
def get_checkpoint_callback(folder_name):
    checkpoint_dir = os.path.join('models', folder_name, 'checkpoints')
    os.makedirs(checkpoint_dir, exist_ok=True)
    checkpoint_callback = ModelCheckpoint(
        filepath=os.path.join(checkpoint_dir, 'model_epoch_{epoch:04d}_loss_{loss:.4f}_acc_{accuracy:.4f}_val_loss_{val_loss:.4f}_val_acc_{val_accuracy:.4f}.h5'),
        save_best_only=True,
        monitor='val_loss',  # Monitoring validation loss
        mode='min',
        save_weights_only=False,  # Save entire model
        verbose=config.VERBOSE_LEVEL
    )
    return checkpoint_callback

# Define EarlyStopping callback
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',  # Metric to monitor (e.g., validation loss)
    patience=config.PATIENCE,           # Number of epochs with no improvement after which training will be stopped
    restore_best_weights=True  # Restore the model weights from the epoch with the best value of the monitored metric
)

# TRAINING TIME -----------------------------------
# Create a new directory for models
os.makedirs('models', exist_ok=True)

model = get_model()
start_datetime = datetime.datetime.now()
current_model_folder_name = f'model_{start_datetime.strftime("%Y-%m-%d_%H-%M-%S")}'

# FIT THE MODEL
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=f'models/{current_model_folder_name}/logs')

# Train the model using the training generator
history = model.fit(
    train_generator,
    epochs=config.EPOCHS,  # Specify the number of training epochs
    validation_data=val_generator,
    verbose=config.VERBOSE_LEVEL,  # You can adjust the verbosity level
    callbacks=[tensorboard_callback, get_checkpoint_callback(current_model_folder_name), early_stopping]
)
finish_datetime = datetime.datetime.now()

# EVAL AND SAVE TIME -----------------------------------
eval(model, test_generator, history, start_datetime, finish_datetime)
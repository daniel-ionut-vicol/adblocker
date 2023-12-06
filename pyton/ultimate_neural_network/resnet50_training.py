import os
import datetime
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.model_selection import train_test_split

# -----------
from eval import eval
from utils import is_image_corrupt

# GPU setup configuration 
tf.keras.backend.clear_session()
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

strategy = tf.distribute.MirroredStrategy()
print(f"Number of GPUs: {strategy.num_replicas_in_sync}")

# Constants from Environment Variables
IMAGE_SIZE = int(os.environ.get("IMAGE_SIZE", 224))
# Constants from Environment Variables for Image Limits
AD_IMAGE_LIMIT = os.environ.get("AD_IMAGE_LIMIT", "all")
NONAD_IMAGE_LIMIT = os.environ.get("NONAD_IMAGE_LIMIT", "all")
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", 32))
EPOCHS = int(os.environ.get("EPOCHS", 10))
PATIENCE = int(os.environ.get("PATIENCE", 20))
DATASET_PATH = os.environ.get("DATASET_PATH", "/app/dataset")
VERBOSE_LEVEL = int(os.environ.get("VERBOSE_LEVEL", 1))

config = {
    'IMAGE_SIZE': IMAGE_SIZE,
    'BATCH_SIZE': BATCH_SIZE,
    'EPOCHS': EPOCHS,
    'PATIENCE': PATIENCE,
    'DATASET_PATH': DATASET_PATH,
    'VERBOSE_LEVEL': VERBOSE_LEVEL,
    'AD_IMAGE_LIMIT': AD_IMAGE_LIMIT,
    'NONAD_IMAGE_LIMIT': NONAD_IMAGE_LIMIT
}

with strategy.scope():
    base_model = ResNet50(weights='imagenet', include_top=False)
    for layer in base_model.layers:
        layer.trainable = False

    x = GlobalAveragePooling2D()(base_model.output)
    x = Dense(1024, activation='relu')(x)
    predictions = Dense(1, activation='sigmoid')(x)
    model = Model(inputs=base_model.input, outputs=predictions)
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
def collect_image_paths(root_dir, label, image_limit):
    file_paths = []
    labels = []
    corrupt_images_log = "corrupt_images.log"
    image_count = 0

    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if image_limit != "all" and image_count >= int(image_limit):
                break

            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(subdir, file)

                if is_image_corrupt(file_path):
                    with open(corrupt_images_log, "a") as log:
                        log.write(file_path + "\n")
                    continue

                file_paths.append(file_path)
                labels.append(label)
                image_count += 1

    return file_paths, labels

# Collect image paths and labels
ad_paths, ad_labels = collect_image_paths(os.path.join(DATASET_PATH, 'ad'), 0, AD_IMAGE_LIMIT)
nonad_paths, nonad_labels = collect_image_paths(os.path.join(DATASET_PATH, 'nonAd'), 1, NONAD_IMAGE_LIMIT)

file_paths = ad_paths + nonad_paths
labels = ad_labels + nonad_labels

train_paths, val_paths, train_labels, val_labels = train_test_split(file_paths, labels, test_size=0.2, random_state=42)

train_generator = custom_generator(train_paths, train_labels, BATCH_SIZE, (IMAGE_SIZE, IMAGE_SIZE))
val_generator = custom_generator(val_paths, val_labels, BATCH_SIZE, (IMAGE_SIZE, IMAGE_SIZE))

train_steps = len(train_paths) // BATCH_SIZE
val_steps = len(val_paths) // BATCH_SIZE

# CALLBACKS -----------------------------------
# Define a callback for dynamic checkpoint naming and specific folder
def get_checkpoint_callback(folder_name):
    checkpoint_dir = os.path.join("models", folder_name, "checkpoints")
    os.makedirs(checkpoint_dir, exist_ok=True)
    checkpoint_callback = ModelCheckpoint(
        filepath=os.path.join(
            checkpoint_dir,
            "model_epoch_{epoch:04d}_loss_{loss:.4f}_acc_{accuracy:.4f}_val_loss_{val_loss:.4f}_val_acc_{val_accuracy:.4f}.h5",
        ),
        save_best_only=True,
        monitor="val_loss",  # Monitoring validation loss
        mode="min",
        save_weights_only=False,  # Save entire model
        verbose=VERBOSE_LEVEL,
    )
    return checkpoint_callback


# Define EarlyStopping callback
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",  # Metric to monitor (e.g., validation loss)
    patience=PATIENCE,  # Number of epochs with no improvement after which training will be stopped
    restore_best_weights=True,  # Restore the model weights from the epoch with the best value of the monitored metric
)

# Create a new directory for models
os.makedirs("models", exist_ok=True)

start_datetime = datetime.datetime.now()
current_model_folder_name = f'model_{start_datetime.strftime("%Y-%m-%d_%H-%M-%S")}'

tensorboard_callback = tf.keras.callbacks.TensorBoard(
    log_dir=f"models/{current_model_folder_name}/logs"
)

# Fit the model
history = model.fit(
    train_generator,
    steps_per_epoch=train_steps,
    epochs=EPOCHS,
    validation_data=val_generator,
    validation_steps=val_steps,
    verbose=VERBOSE_LEVEL,
    callbacks=[
        tensorboard_callback,
        get_checkpoint_callback(current_model_folder_name),
        early_stopping,
    ],
)

finish_datetime = datetime.datetime.now()

eval(model, val_generator, history, start_datetime, finish_datetime, config)
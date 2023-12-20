import sys
sys.path.append("..")

import os
import datetime
import tensorflow as tf
from sklearn.model_selection import train_test_split
# -----------
from models.resnet50 import resNet50
from helpers.eval import eval
from helpers.utils import collect_image_paths
from generators.resnet50_generator import custom_generator
from helpers.callbacks import checkpoint_callback, early_stopping, tensorboard_callback
import config

print(config)

# GPU setup configuration 
tf.keras.backend.clear_session()
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

strategy = tf.distribute.MirroredStrategy()
print(f"Number of GPUs: {strategy.num_replicas_in_sync}")

model = resNet50(strategy)

# Collect image paths and labels
ad_paths, ad_labels = collect_image_paths(os.path.join(config.DATASET_PATH, 'ad'), 0, config.AD_IMAGE_LIMIT)
nonad_paths, nonad_labels = collect_image_paths(os.path.join(config.DATASET_PATH, 'nonAd'), 1, config.NONAD_IMAGE_LIMIT)

file_paths = ad_paths + nonad_paths
labels = ad_labels + nonad_labels

train_paths, val_paths, train_labels, val_labels = train_test_split(file_paths, labels, test_size=0.2, random_state=42)

train_generator = custom_generator(train_paths, train_labels, config.BATCH_SIZE, (config.IMAGE_SIZE, config.IMAGE_SIZE))
val_generator = custom_generator(val_paths, val_labels, config.BATCH_SIZE, (config.IMAGE_SIZE, config.IMAGE_SIZE))

train_steps = len(train_paths) // config.BATCH_SIZE
val_steps = len(val_paths) // config.BATCH_SIZE

# Create a new directory for models
os.makedirs("/home/models", exist_ok=True)

start_datetime = datetime.datetime.now()
current_model_folder_name = f'model_{start_datetime.strftime("%Y-%m-%d_%H-%M-%S")}'

# Fit the model
history = model.fit(
    train_generator,
    steps_per_epoch=train_steps,
    epochs=config.EPOCHS,
    validation_data=val_generator,
    validation_steps=val_steps,
    verbose=config.VERBOSE_LEVEL,
    callbacks=[
        tensorboard_callback,
        checkpoint_callback(current_model_folder_name),
        early_stopping,
    ],
)

finish_datetime = datetime.datetime.now()

eval(model, val_generator, history, start_datetime, finish_datetime)
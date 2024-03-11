import os
import sys
import pickle
import json
import datetime
import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
# -----------
sys.path.append("..")
sys.path.append(os.getcwd())
from models.get_model import get_model
from helpers.eval import eval
from helpers.utils import collect_image_paths
from generators.ultimate_generator import Generator 
from helpers.callbacks import checkpoint_callback, csv_logger_callback, early_stopping, tensorboard_callback
import config

# GPU setup configuration 
tf.keras.backend.clear_session()
gpus = tf.config.experimental.list_physical_devices('GPU')

for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

strategy = tf.distribute.MirroredStrategy()
print(f"Number of GPUs: {strategy.num_replicas_in_sync}")

model = get_model(strategy)

# Collect image paths and labels
ad_paths, ad_labels = collect_image_paths(os.path.join(config.DATASET_PATH, 'ad'), 0, config.AD_IMAGE_LIMIT)
nonad_paths, nonad_labels = collect_image_paths(os.path.join(config.DATASET_PATH, 'nonAd'), 1, config.NONAD_IMAGE_LIMIT)

file_paths = ad_paths + nonad_paths
labels = ad_labels + nonad_labels

# Calculate the test ratio in terms of the train + val set
test_ratio = config.TEST_RATIO / (config.TRAIN_RATIO + config.VAL_RATIO)
# First split to separate out the test set
train_val_paths, test_paths, train_val_labels, test_labels = train_test_split(file_paths, labels, test_size=config.TEST_RATIO, random_state=42)
# Second split to separate out the train and val sets
train_paths, val_paths, train_labels, val_labels = train_test_split(train_val_paths, train_val_labels, test_size=test_ratio, random_state=42)

train_generator = Generator(train_paths, train_labels, config.BATCH_SIZE)
val_generator = Generator(val_paths, val_labels, config.BATCH_SIZE, is_training=False)
# Assuming you have test_paths and test_labels
test_generator = Generator(test_paths, test_labels, config.BATCH_SIZE, is_training=False)

train_steps = len(train_paths) // config.BATCH_SIZE
val_steps = len(val_paths) // config.BATCH_SIZE
test_steps = len(test_paths) // config.BATCH_SIZE

start_datetime = datetime.datetime.now()

current_model_folder_name = f'model_{start_datetime.strftime("%Y-%m-%d_%H-%M-%S")}'
# Create a new directory for models
os.makedirs(f"{os.environ['DATA']}/cnn_training/models/{current_model_folder_name}", exist_ok=True)
# Define a file path where you want to save the test_paths and test_labels
output_file = f'{os.environ["DATA"]}/cnn_training/models/{current_model_folder_name}/test_data.pkl'
# Open the file in write mode
with open(output_file, 'wb') as file:
    # Write the test_paths and test_labels to the file
    pickle.dump((test_paths, test_labels), file)

# Save the configuration data and dataset sizes to config.json
config_data = {
    'GPUS_NO': strategy.num_replicas_in_sync,
    'MODEL': config.MODEL,
    'IMAGE_SIZE': config.IMAGE_SIZE,
    'BATCH_SIZE': config.BATCH_SIZE,
    'EPOCHS': config.EPOCHS,
    'PATIENCE': config.PATIENCE,
    'AD_IMAGE_LIMIT': config.AD_IMAGE_LIMIT,
    'NONAD_IMAGE_LIMIT': config.NONAD_IMAGE_LIMIT,
    'Train Images': len(train_paths),
    'Validation Images': len(val_paths),
    'Test Images': len(test_paths),
    "TRAIN_RATIO": config.TRAIN_RATIO,
    "VAL_RATIO": config.VAL_RATIO,
    "TEST_RATIO": config.TEST_RATIO,
    "USE_AUGMENTATION": config.USE_AUGMENTATION,
    "ROTATION_RANGE": config.ROTATION_RANGE,
    "WIDTH_SHIFT_RANGE": config.WIDTH_SHIFT_RANGE,
    "HEIGHT_SHIFT_RANGE": config.HEIGHT_SHIFT_RANGE,
    "BRIGHTNESS_RANGE": config.BRIGHTNESS_RANGE,
    "HORIZONTAL_FLIP": config.HORIZONTAL_FLIP,
    "FILL_MODE": config.FILL_MODE,
    "RESCALE_NUMERATOR": config.RESCALE_NUMERATOR,
    "RESCALE_DENOMINATOR": config.RESCALE_DENOMINATOR
}
with open(f'{os.environ["DATA"]}/cnn_training/models/{current_model_folder_name}/config.json', 'w') as f:
    json.dump(config_data, f)

# Fit the model
history = model.fit(
    train_generator,
    steps_per_epoch=train_steps,
    epochs=config.EPOCHS,
    validation_data=val_generator,
    validation_steps=val_steps,
    verbose=config.VERBOSE_LEVEL,
    callbacks=[
        tensorboard_callback(current_model_folder_name),
        checkpoint_callback(current_model_folder_name),
        csv_logger_callback(current_model_folder_name),
        early_stopping,
    ],
)

finish_datetime = datetime.datetime.now()

with open(output_file, 'wb') as file:
    # Write the data to the file
    pickle.dump((test_steps, start_datetime, finish_datetime), file)

# Convert the history.history dict to a pandas DataFrame
hist_df = pd.DataFrame(history.history)

# Save to csv
hist_csv_file = f'{os.environ["DATA"]}/cnn_training/models/{current_model_folder_name}/history.csv'
with open(hist_csv_file, mode='w') as f:
    hist_df.to_csv(f)

eval(model, test_generator, test_steps, history, start_datetime, finish_datetime)

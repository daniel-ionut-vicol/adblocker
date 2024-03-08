import os
import sys
import pickle
sys.path.append("..")
sys.path.append(os.getcwd())

import datetime
import tensorflow as tf
from sklearn.model_selection import train_test_split
import pandas as pd
# -----------
from models.resnet50 import resNet50
from helpers.eval import eval
from helpers.utils import collect_image_paths
from generators.ultimate_generator import Generator 
from helpers.callbacks import checkpoint_callback, early_stopping, tensorboard_callback
import config

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

train_paths, test_paths, train_labels, test_labels = train_test_split(file_paths, labels, test_size=0.2, random_state=42)
train_paths, val_paths, train_labels, val_labels = train_test_split(train_paths, train_labels, test_size=0.25, random_state=42)  # 0.25 x 0.8 = 0.2

train_generator = Generator(train_paths, train_labels, config.BATCH_SIZE)
val_generator = Generator(val_paths, val_labels, config.BATCH_SIZE)
# Assuming you have test_paths and test_labels
test_generator = Generator(test_paths, test_labels, config.BATCH_SIZE)

train_steps = len(train_paths) // config.BATCH_SIZE
val_steps = len(val_paths) // config.BATCH_SIZE
test_steps = len(test_paths) // config.BATCH_SIZE

print('Train Paths:', len(train_paths))
print('Train Labels:', len(train_labels))
print('Validation Paths:', len(val_paths))
print('Validation Labels:', len(val_labels))
print('Test Paths:', len(test_paths))
print('Test Labels:', len(test_labels))

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

# Print a confirmation message
print(f'Test paths and labels saved to {output_file}')

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
import sys
sys.path.append("..")

import os
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger
import config

# CALLBACKS -----------------------------------
# Define a callback for dynamic checkpoint naming and specific folder
def checkpoint_callback(folder_name):
    checkpoint_dir = os.path.join(f"{os.environ['DATA']}/cnn_training/models", folder_name, "checkpoints")
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
        verbose=config.VERBOSE_LEVEL,
    )
    return checkpoint_callback


# Define EarlyStopping callback
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",  # Metric to monitor (e.g., validation loss)
    patience=config.PATIENCE,  # Number of epochs with no improvement after which training will be stopped
    restore_best_weights=True,  # Restore the model weights from the epoch with the best value of the monitored metric
)

def tensorboard_callback(current_model_folder_name):
    return tf.keras.callbacks.TensorBoard(log_dir=f"{os.environ['DATA']}/cnn_training/models/{current_model_folder_name}/logs"
)

# Create a CSVLogger callback
def csv_logger_callback(current_model_folder_name):
    csv_logger = CSVLogger(f"{os.environ['DATA']}/cnn_training/models/{current_model_folder_name}/history.csv", append=True)
    return csv_logger
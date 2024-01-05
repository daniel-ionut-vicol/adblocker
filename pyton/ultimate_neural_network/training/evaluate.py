import os
import sys
sys.path.append("..")
sys.path.append(os.getcwd())

import tensorflow as tf

from helpers.utils import collect_image_paths
from generators.resnet50_generator import custom_generator
import config

from helpers.custom_metrics import precision, recall, f1_score

model = tf.keras.models.load_model("/mnt/data/mlserver/cnn_training/models/model_2024-01-05_10-00-35/saved_model/h5/model.h5", custom_objects={'precision': precision, 'recall': recall, 'f1_score': f1_score})

test_paths, test_labels = collect_image_paths("/mnt/data/mlserver/newdataset/ad", 0, 1500)
test_generator = custom_generator(test_paths, test_labels, config.BATCH_SIZE, (config.IMAGE_SIZE, config.IMAGE_SIZE))
test_steps = len(test_paths) // config.BATCH_SIZE

def eval(model, test_generator, test_steps):
    print("Starting evaluation...")

    # Evaluate the model on the test data
    loss, accuracy, precision, recall, f1_score = model.evaluate(test_generator, steps=test_steps)

    # Write the metrics to the file
    print('#TRAINING SETTINGS#\n')
    print('-----------------------\n')
    print(f'IMAGE_SIZE={config.IMAGE_SIZE}\n')
    print(f'BATCH_SIZE={config.BATCH_SIZE}\n')
    print(f'EPOCHS={config.EPOCHS}\n')
    print(f'PATIENCE={config.PATIENCE}\n\n')
    print(f'AD_IMAGE_LIMIT={config.AD_IMAGE_LIMIT}\n\n')
    print(f'NONAD_IMAGE_LIMIT={config.NONAD_IMAGE_LIMIT}\n\n')
    print('#METRICS#\n')
    print('-----------------------\n')
    print(f'Loss: {loss}\n')
    print(f'Accuracy: {accuracy}\n')
    print(f'Precision: {precision}\n')
    print(f'Recall: {recall}\n')
    print(f'F1-score: {f1_score}\n')
    print('-----------------------\n\n')
    print("Evaluation completed...")

eval(model, test_generator, test_steps)
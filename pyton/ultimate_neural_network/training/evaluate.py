import os
import sys
import json
import pickle
import tensorflow as tf

sys.path.append("..")
sys.path.append(os.getcwd())
from helpers.custom_metrics import F1Score
from generators.ultimate_generator import Generator

def eval(model, test_generator, test_steps):
    print("Starting evaluation...")

    # Evaluate the model on the test data
    loss, accuracy, precision, recall, f1_score = model.evaluate(test_generator, steps=test_steps)

    # Change the filename to match the model name
    results_file = os.path.join(model_dir, f'{model_name}_evaluation_results.txt')
    # Write the metrics to the file
    with open(results_file, 'w') as f:
        f.write('#TRAINING SETTINGS#\n')
        f.write('-----------------------\n')
        f.write(f'GPUS_NO={config["GPUS_NO"]}\n')
        f.write(f'IMAGE_SIZE={config["IMAGE_SIZE"]}\n')
        f.write(f'BATCH_SIZE={config["BATCH_SIZE"]}\n')
        f.write(f'EPOCHS={config["EPOCHS"]}\n')
        f.write(f'PATIENCE={config["PATIENCE"]}\n\n')
        f.write(f'AD_IMAGE_LIMIT={config["AD_IMAGE_LIMIT"]}\n\n')
        f.write(f'NONAD_IMAGE_LIMIT={config["NONAD_IMAGE_LIMIT"]}\n\n')
        f.write('#METRICS#\n')
        f.write('-----------------------\n')
        f.write(f'Loss: {loss}\n')
        f.write(f'Accuracy: {accuracy}\n')
        f.write(f'Precision: {precision}\n')
        f.write(f'Recall: {recall}\n')
        f.write(f'F1-score: {f1_score}\n')
        f.write('-----------------------\n\n')
    print("Evaluation completed...")

if __name__ == "__main__":
    model_path = os.path.join('/mnt/data/mlserver/cnn_training/', sys.argv[1])
    model_dir = os.path.dirname(os.path.dirname(model_path))  # Go up one level
    model_name = os.path.splitext(os.path.basename(model_path))[0]  # Get the model name without extension
    model = tf.keras.models.load_model(model_path, custom_objects={'F1Score': F1Score})

    # Load test paths from the pickle file
    with open(os.path.join(model_dir, 'test_data.pkl'), 'rb') as f:
        test_paths, test_labels = pickle.load(f)

    test_labels = tf.cast(test_labels, dtype=tf.float32)

    # Load config from the json file
    with open(os.path.join(model_dir, 'config.json'), 'r') as f:
        config = json.load(f)

    test_generator = Generator(test_paths, test_labels, config["BATCH_SIZE"], image_min_side=config["IMAGE_SIZE"], is_training=False)
    test_steps = len(test_paths) // int(config["BATCH_SIZE"])

    os.chdir(model_dir)  # Change the current working directory to the model folder
    eval(model, test_generator, test_steps)

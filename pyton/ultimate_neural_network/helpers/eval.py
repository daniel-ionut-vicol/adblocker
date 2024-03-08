import os
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflowjs as tfjs
import config

def saveMetric(epochs, metric_values, val_metric_values, metric_name, current_model_folder_name):
    plt.figure(figsize=(10, 6))
    plt.plot(epochs, metric_values, color='teal', marker='o', label=f'Training {metric_name}')
    plt.plot(epochs, val_metric_values, color='orange', marker='o', label=f'Validation {metric_name}')
    
    plt.title(f'{metric_name} (Training vs Validation)', fontsize=20)
    plt.xlabel('Epochs', fontsize=14)
    plt.ylabel(metric_name, fontsize=14)
    plt.legend()
    plt.grid(True)
    
    save_path = os.path.join(os.environ["DATA"], 'cnn_training', 'models', current_model_folder_name, 'metrics', f'{metric_name}_plot.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.show()

def saveModel(model, current_model_folder_name, name='model'):
    keras_save_path = os.path.join(os.environ["DATA"], 'cnn_training', 'models', current_model_folder_name, 'saved_model', 'keras', f'{name}.keras')
    tf_save_path = os.path.join(os.environ["DATA"], 'cnn_training', 'models', current_model_folder_name, 'saved_model', 'tf', name)
    h5_save_path = os.path.join(os.environ["DATA"], 'cnn_training', 'models', current_model_folder_name, 'saved_model', 'h5', f'{name}.h5')

    os.makedirs(os.path.dirname(keras_save_path), exist_ok=True)
    os.makedirs(os.path.dirname(tf_save_path), exist_ok=True)
    os.makedirs(os.path.dirname(h5_save_path), exist_ok=True)

    tfjs.converters.save_keras_model(model, os.path.join(os.environ["DATA"], 'cnn_training', 'models', current_model_folder_name, 'saved_model', 'tfjs'))
    tf.keras.models.save_model(model, keras_save_path)
    tf.keras.models.save_model(model, tf_save_path, save_format='tf')
    tf.keras.models.save_model(model, h5_save_path, save_format='h5')

def eval(model, test_generator, test_steps, history, start_datetime, finish_datetime):
    print("Starting evaluation...")
    current_model_folder_name = f'model_{start_datetime.strftime("%Y-%m-%d_%H-%M-%S")}'

    # Evaluate the model on the test data
    loss, accuracy, precision, recall, f1_score = model.evaluate(test_generator, steps=test_steps)

    # Define a file path where you want to save the metrics
    output_file = os.path.join(os.environ["DATA"], 'cnn_training', 'models', current_model_folder_name, 'evaluation_results.txt')

    # Open the file in write mode
    with open(output_file, 'w') as file:
        # Write the metrics to the file
        file.write('#TRAINING SETTINGS#\n')
        file.write('-----------------------\n')
        file.write(f'IMAGE_SIZE={config.IMAGE_SIZE}\n')
        file.write(f'BATCH_SIZE={config.BATCH_SIZE}\n')
        file.write(f'EPOCHS={config.EPOCHS}\n')
        file.write(f'PATIENCE={config.PATIENCE}\n\n')
        file.write(f'AD_IMAGE_LIMIT={config.AD_IMAGE_LIMIT}\n\n')
        file.write(f'NONAD_IMAGE_LIMIT={config.NONAD_IMAGE_LIMIT}\n\n')
        file.write('#METRICS#\n')
        file.write('-----------------------\n')
        file.write(f'Loss: {loss}\n')
        file.write(f'Accuracy: {accuracy}\n')
        file.write(f'Precision: {precision}\n')
        file.write(f'Recall: {recall}\n')
        file.write(f'F1-score: {f1_score}\n')
        file.write('-----------------------\n\n')
        file.write(f'Training took: {finish_datetime-start_datetime}')

    # Close the file
    file.close()

    # Print a confirmation message
    print(f'Evaluation metrics saved to {output_file}')

    os.makedirs(os.path.join(os.environ["DATA"], 'cnn_training', 'models', current_model_folder_name, 'metrics'), exist_ok=True)

    try:
        print("Saving metrics...")
        # Save metrics for loss and accuracy
        num_epochs = len(history.history['loss'])

        saveMetric(range(1, num_epochs + 1), history.history['loss'], history.history['val_loss'], 'Loss', current_model_folder_name)
        saveMetric(range(1, num_epochs + 1), history.history['accuracy'], history.history['val_accuracy'], 'Accuracy', current_model_folder_name)
        # Save metrics for precision, recall, and f1_score
        saveMetric(range(1, num_epochs + 1), history.history['precision'], history.history['val_precision'], 'Precision', current_model_folder_name)
        saveMetric(range(1, num_epochs + 1), history.history['recall'], history.history['val_recall'], 'Recall', current_model_folder_name)
        saveMetric(range(1, num_epochs + 1), history.history['f1_score'], history.history['val_f1_score'], 'F1 Score', current_model_folder_name)
        
    except Exception as e:
        print("Could not save the metrics")
        print(e)

    try:
        saveModel(model, current_model_folder_name)
        print("Model saved at: ", os.path.join(current_model_folder_name, "saved_model"))
    except Exception as e:
        print("Could not save the model")
        print(e)
        
    print("Evaluation completed...")

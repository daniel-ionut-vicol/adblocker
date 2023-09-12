import os
from matplotlib import pyplot as plt
import tensorflow as tf
import tensorflowjs as tfjs
from config import IMAGE_SIZE, BATCH_SIZE, EPOCHS, PATIENCE

def eval(model, test_generator, history, start_datetime, finish_datetime):
    current_model_folder_name = f'model_{start_datetime.strftime("%Y-%m-%d_%H-%M-%S")}'

    # Evaluate the model on the test data
    loss, accuracy, precision, recall, f1_score = model.evaluate(test_generator)

    # Define a file path where you want to save the metrics
    output_file = f'models/{current_model_folder_name}/training_results.txt'

    # Open the file in write mode
    with open(output_file, 'w') as file:
        # Write the metrics to the file
        file.write('Training settings:\n')
        file.write(f'IMAGE_SIZE={IMAGE_SIZE}\n')
        file.write(f'BATCH_SIZE={BATCH_SIZE}\n')
        file.write(f'EPOCHS={EPOCHS}\n')
        file.write(f'PATIENCE={PATIENCE}\n')
        file.write('-----------------------\n')
        file.write(f'Loss: {loss}\n')
        file.write(f'Accuracy: {accuracy}\n')
        file.write(f'Precision: {precision}\n')
        file.write(f'Recall: {recall}\n')
        file.write(f'F1-score: {f1_score}\n')
        file.write('-----------------------\n')
        file.write(f'Training took: {finish_datetime-start_datetime}')

    # Close the file
    file.close()

    # Print a confirmation message
    print(f'Evaluation metrics saved to {output_file}')

    os.makedirs(f'/models/{current_model_folder_name}/metrics/', exist_ok=True)

    def saveMetric(metric):
        # Plot the loss over epochs
        fig = plt.figure()
        plt.plot(history.history[metric], color='teal', label=metric)
        plt.plot(history.history[f'val_{metric}'], color='orange', label=f'val_{metric}')
        fig.suptitle(metric, fontsize=20)
        plt.legend(loc="upper left")
        plt.savefig(f'/models/{current_model_folder_name}/metrics/tragining_{metric}.png', bbox_inches='tight')

    def saveModel(name='model'):
        os.makedirs(f'/models/{current_model_folder_name}/saved_model/keras/', exist_ok=True)
        os.makedirs(f'/models/{current_model_folder_name}/saved_model/tf/', exist_ok=True)
        os.makedirs(f'/models/{current_model_folder_name}/saved_model/h5/', exist_ok=True)
        
        tfjs.converters.save_keras_model(model, f'/models/{current_model_folder_name}/saved_model/tfjs/' )
        tf.keras.models.save_model(model, f'/models/{current_model_folder_name}/saved_model/keras/{name}.keras')
        tf.keras.models.save_model(model, f'/models/{current_model_folder_name}/saved_model/tf/{name}', save_format='tf')
        tf.keras.models.save_model(model, f'/models/{current_model_folder_name}/saved_model/h5/{name}.h5', save_format='h5')

    saveMetric('loss')
    saveMetric('accuracy')
    saveModel()
import os
import datetime
import numpy as np
import tensorflow as tf
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
from matplotlib import pyplot as plt
# ---------------
from ultimate_generator import Generator
from ultimate_model import model

# Load environment variables from the .env file
load_dotenv()

# CHECK the GPU's state
print("The gpu's available are", tf.config.experimental.list_physical_devices('GPU'))


# Build the model
model.build(input_shape=(int(os.environ['BATCH_SIZE']), int(os.environ['IMAGE_SIZE']), int(os.environ['IMAGE_SIZE']), 3))
# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

print("Model compilation summary", model.summary())

def load_image_paths_labels(DATASET_PATH=os.environ['DATASET_PATH']):
    classes = []
    image_paths = []
    image_labels = []

    for class_name in os.listdir(DATASET_PATH):
        class_path = os.path.join(DATASET_PATH, class_name)
        if os.path.isdir(class_path):
            for root, _, files in os.walk(class_path):
                for file in files:
                    if file.endswith(".png"):  # Only collect PNG files
                        if class_name not in classes:
                            classes.append(class_name)
    lb = preprocessing.LabelBinarizer()
    lb.fit(classes)
    image_labels = np.array(lb.transform(image_labels), dtype='int')
    assert len(image_paths) == len(image_labels)

    return image_paths, image_labels


# Load image paths and labels
image_paths, image_labels = load_image_paths_labels(os.environ['DATASET_PATH'])

# Split the data into training, validation, and test sets
train_paths, temp_paths, train_labels, temp_labels = train_test_split(image_paths, image_labels, test_size=0.2, random_state=42)
val_paths, test_paths, val_labels, test_labels = train_test_split(temp_paths, temp_labels, test_size=0.5, random_state=42)

# Create generators for training, validation, and test sets
train_generator = Generator(train_paths, train_labels, BATCH_SIZE=int(os.environ['BATCH_SIZE']), is_training=True)
val_generator = Generator(val_paths, val_labels, BATCH_SIZE=int(os.environ['BATCH_SIZE']), is_training=False)
test_generator = Generator(test_paths, test_labels, BATCH_SIZE=int(os.environ['BATCH_SIZE']), is_training=False)

# FIT THE MODEL
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=os.environ['LOG_DIR'])

start_datetime = datetime.datetime.now()

# Train the model using the training generator
history = model.fit(
    train_generator,
    epochs=int(os.environ['EPOCHS']),  # Specify the number of training epochs
    validation_data=val_generator,
    verbose=int(os.environ['VERBOSE_LEVEL']),  # You can adjust the verbosity level
    callbacks=[tensorboard_callback]
)

finish_datetime = datetime.datetime.now()

# Evaluate the model on the test data
test_loss, test_accuracy = model.evaluate(test_generator)
print(f'Test Loss: {test_loss:.4f}')
print(f'Test Accuracy: {test_accuracy:.4f}')
print(f'---Training took:', finish_datetime - start_datetime)

# Create a new directory for models
os.makedirs('models', exist_ok=True)

current_model_folder_name = f'model_{start_datetime}-{finish_datetime}'
os.makedirs(f'/models/{current_model_folder_name}/metrics', exist_ok=True)

# Plot the loss over epochs
fig = plt.figure()
plt.plot(history.history['loss'], color='teal', label='loss')
plt.plot(history.history['val_loss'], color='orange', label='val_loss')
fig.suptitle('Loss', fontsize=20)
plt.legend(loc="upper left")
plt.savefig(f'/models/{current_model_folder_name}/metrics/training_loss.png', bbox_inches='tight')

# Plot the accuracy
fig = plt.figure()
plt.plot(history.history['accuracy'], color='teal', label='accuracy')
plt.plot(history.history['val_accuracy'], color='orange', label='val_accuracy')
fig.suptitle('Accuracy', fontsize=20)
plt.legend(loc="upper left")
plt.savefig(f'/models/{current_model_folder_name}/metrics/training_accuracy.png', bbox_inches='tight')

model.save(f'/models/{current_model_folder_name}/saved_model/keras/model.keras', save_format='keras')
model.save(f'/models/{current_model_folder_name}/saved_model/tf/model', save_format='tf')
model.save(f'/models/{current_model_folder_name}/saved_model/h5/model.h5', save_format='h5')

import os
import datetime
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import backend as K
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import ModelCheckpoint
from transformers import CLIPModel, CLIPProcessor

# -----------
from eval import eval
from utils import is_image_corrupt

IMAGE_SIZE = int(os.getenv("IMAGE_SIZE", 224))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 32))
EPOCHS = int(os.getenv("EPOCHS", 10))
PATIENCE = int(os.getenv("PATIENCE", 20))
DATASET_PATH = os.getenv("DATASET_PATH", "/app/dataset")
VERBOSE_LEVEL = int(os.getenv("VERBOSE_LEVEL", 1))
TEXT_INPUT_SIZE = int(os.getenv("TEXT_INPUT_SIZE", 1))

config = {
    IMAGE_SIZE,
    BATCH_SIZE,
    EPOCHS,
    PATIENCE,
    DATASET_PATH,
    VERBOSE_LEVEL,
    TEXT_INPUT_SIZE,
}

# GPU setup configuration
K.clear_session()

gpus = tf.config.experimental.list_physical_devices("GPU")
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)

# Use MirroredStrategy to utilize all GPUs
strategy = tf.distribute.MirroredStrategy()
print(f"Number of GPUs: {strategy.num_replicas_in_sync}")

# Define CLIP model and processor
with strategy.scope():
    # Load the pre-trained CLIP model and processor
    clip_model = CLIPModel.from_pretrained(
        "./pretrained/clip-vit-base-patch32", from_tf=False
    )
    clip_processor = CLIPProcessor.from_pretrained("./pretrained/clip-vit-base-patch32")

    # Define the input layers for images and text
    image_input = Input(shape=(IMAGE_SIZE, IMAGE_SIZE, 3), name="image_input")
    text_input = Input(shape=(TEXT_INPUT_SIZE,), dtype=tf.string, name="text_input")

    # Process images and text
    image_features = clip_model.pixel_values(image_input)
    text_features = clip_model.embed_text(text_input)

    # Combine image and text features
    combined_features = tf.concat([image_features, text_features], axis=-1)

    # Add a classification head for binary classification
    predictions = Dense(1, activation="sigmoid")(combined_features)

    # Create the model
    model = Model(inputs=[image_input, text_input], outputs=predictions)

    # Compile the model with binary cross-entropy loss
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )


# Function to load and preprocess a single image
def preprocess_image(image_path, target_size):
    img = load_img(image_path, target_size=target_size)
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    return img


def custom_generator(
    file_paths, labels, batch_size, target_size, processor, text_prompts
):
    num_samples = len(file_paths)
    while True:
        for offset in range(0, num_samples, batch_size):
            batch_paths = file_paths[offset : offset + batch_size]
            batch_labels = labels[offset : offset + batch_size]

            images = [preprocess_image(path, target_size) for path in batch_paths]
            images = np.vstack(images)

            # Map each image to its corresponding text prompt
            batch_texts = [text_prompts[label] for label in batch_labels]

            # Process text inputs
            text_inputs = processor(
                text=batch_texts,
                max_length=TEXT_INPUT_SIZE,
                padding="max_length",
                truncation=True,
                return_tensors="tf",
            ).input_ids

            yield {"image_input": images, "text_input": text_inputs}, np.array(
                batch_labels
            )


def collect_image_paths(root_dir, label):
    file_paths = []
    labels = []
    corrupt_images_log = "corrupt_images.log"  # Log file for corrupt images

    print(f"Scanning directory: {root_dir}")  # Debug print
    for subdir, dirs, files in os.walk(root_dir):
        print(f"Found {len(files)} files in {subdir}")  # Debug print
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                file_path = os.path.join(subdir, file)

                # Check for corrupt images
                if is_image_corrupt(file_path):
                    print(f"Corrupt image detected: {file_path}")
                    with open(corrupt_images_log, "a") as log:
                        log.write(file_path + "\n")
                    continue

                file_paths.append(file_path)
                labels.append(label)

    return file_paths, labels


text_prompts = {
    0: "An image depicting a typical advertisement. It is characterized by vibrant colors and high-contrast lighting to catch the viewer's eye. The composition includes a clear brand logo and a product or service being prominently displayed. There's persuasive text, such as a catchy slogan or a special offer, aimed at encouraging consumer action. Elements like human models, exaggerated emotions, or idealized scenarios are common, emphasizing the product's benefits. The layout is professional, with a focus on aesthetic appeal and strategic placement of text and visuals to guide the viewer's attention.",
    1: "An image representing a non-commercial, everyday scene. It is marked by a more natural and subdued color palette, with lighting that reflects real-world conditions rather than dramatic or staged enhancements. The content is devoid of brand logos, promotional text, or sales pitches. Instead, it might feature landscapes, unposed people, animals, or common objects in their natural state, without any artificial staging. The composition is candid and unstructured, capturing a slice of life or a natural scene without the intention of selling or promoting any product or service.",
}

# Collect image paths and labels
ad_paths, ad_labels = collect_image_paths(
    os.path.join(DATASET_PATH, "ad"), 0
)  # Label for 'Ad'
nonad_paths, nonad_labels = collect_image_paths(
    os.path.join(DATASET_PATH, "nonAd"), 1
)  # Label for 'NonAd'

# Combine the paths and labels
file_paths = ad_paths + nonad_paths
labels = ad_labels + nonad_labels

# Split the data into training and validation sets
train_paths, val_paths, train_labels, val_labels = train_test_split(
    file_paths, labels, test_size=0.2, random_state=42
)

train_generator = custom_generator(
    train_paths,
    train_labels,
    BATCH_SIZE,
    (IMAGE_SIZE, IMAGE_SIZE),
    clip_processor,
    text_prompts,
)
val_generator = custom_generator(
    val_paths,
    val_labels,
    BATCH_SIZE,
    (IMAGE_SIZE, IMAGE_SIZE),
    clip_processor,
    text_prompts,
)

# Assuming 'model' is your compiled model (e.g., based on ResNet50)
# Define the number of steps per epoch for training and validation
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
    epochs=EPOCHS,  # Number of epochs
    validation_data=val_generator,
    validation_steps=val_steps,
    verbose=VERBOSE_LEVEL,  # You can adjust the verbosity level
    callbacks=[
        tensorboard_callback,
        get_checkpoint_callback(current_model_folder_name),
        early_stopping,
    ],
)

finish_datetime = datetime.datetime.now()

eval(model, val_generator, history, start_datetime, finish_datetime, config)
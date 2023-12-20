import sys
sys.path.append("..")

import tensorflow as tf
from transformers import CLIPModel, CLIPProcessor
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense

import config

def clipModel(strategy): 
    # Define CLIP model and processor
    with strategy.scope():
        # Load the pre-trained CLIP model and processor
        clip_model = CLIPModel.from_pretrained(
            "./pretrained/clip-vit-base-patch32", from_tf=False
        )
        clip_processor = CLIPProcessor.from_pretrained("./pretrained/clip-vit-base-patch32")

        # Define the input layers for images and text
        image_input = Input(shape=(config.IMAGE_SIZE, config.IMAGE_SIZE, 3), name="image_input")
        text_input = Input(shape=(config.TEXT_INPUT_SIZE,), dtype=tf.string, name="text_input")

        # Process images and text
        image_features = clip_model.pixel_values(image_input)
        text_features = clip_model.embed_text(text_input)

        # Combine image and text features
        combined_features = tf.concat([image_features, text_features], axis=-1)

        # Add a classification head for binary classification
        predictions = Dense(1, activation="sigmoid")(combined_features)

        # Create the model
        model = Model(inputs=[image_input, text_input], outputs=predictions)

        return model
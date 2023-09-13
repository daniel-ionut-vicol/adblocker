import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

def visualise_model_layers(model, image_path):
    # Load and preprocess the RGB image
    img = cv2.imread(image_path)  # Load as RGB image
    img = cv2.resize(img, (256, 256))  # Resize to match your model's input size
    img = img / 255.0  # Normalize the pixel values to the range [0, 1]
    img = np.expand_dims(img, axis=0)  # Add batch dimension

    layer_names = [layer.name for layer in model.layers]

    os.makedirs("layer_features_visualisation", exist_ok=True)

    for layer_name in layer_names:
        # Create a submodel that extracts feature maps from a specific layer
        feature_extractor = tf.keras.Model(inputs=model.inputs, outputs=model.get_layer(layer_name).output)

        # Pass the preprocessed image through the feature extractor
        feature_maps = feature_extractor.predict(img)

        # Visualize the feature maps
        num_feature_maps = feature_maps.shape[3]  # Number of feature maps in the selected layer

        # Calculate the number of rows and columns in the subplot grid
        num_rows = int(np.ceil(np.sqrt(num_feature_maps)))
        num_cols = int(np.ceil(num_feature_maps / num_rows))

        # Create subplots with dynamic grid size
        plt.figure(figsize=(100, 100))
        for i in range(num_feature_maps):
            ax = plt.subplot(num_rows, num_cols, i + 1)
            ax.set_xticks([])
            ax.set_yticks([])
            if i < num_feature_maps:
                plt.imshow(feature_maps[0, :, :, i], cmap='viridis')  # Adjust the colormap as needed
        plt.savefig(f'layer_features_visualisation/{layer_names.index(layer_name)+1}. {layer_name}_{image_path}')
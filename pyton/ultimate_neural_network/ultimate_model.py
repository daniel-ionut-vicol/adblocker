import os
import tensorflow as tf

model = tf.keras.Sequential([
    # Convolutional layer with 32 filters and a kernel size of 3
    tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(os.environ['IMAGE_SIZE'], os.environ['IMAGE_SIZE'], 3)),
    # Batch normalization layer to normalize the inputs of the convolutional layer
    tf.keras.layers.BatchNormalization(),
    # Max-pooling layer with a pool size of 2
    tf.keras.layers.MaxPooling2D(),
    # Dropout layer with a rate of 0.2 to randomly drop out 20% of the units
    tf.keras.layers.Dropout(0.2),
    # Convolutional layer with 64 filters and a kernel size of 3
    tf.keras.layers.Conv2D(64, 3, activation='relu'),
    # Batch normalization layer to normalize the inputs of the convolutional layer
    tf.keras.layers.BatchNormalization(),
    # Max-pooling layer with a pool size of 2
    tf.keras.layers.MaxPooling2D(),
    # Dropout layer with a rate of 0.2 to randomly drop out 20% of the units
    tf.keras.layers.Dropout(0.2),
    # Flatten layer to convert the feature maps into a 1D tensor
    tf.keras.layers.Flatten(),
    # Fully connected layer with 128 units and ReLU activation
    tf.keras.layers.Dense(128, activation='relu'),
    # Batch normalization layer to normalize the inputs of the fully connected layer
    tf.keras.layers.BatchNormalization(),
    # Dropout layer with a rate of 0.5 to randomly drop out 50% of the units
    tf.keras.layers.Dropout(0.5),
    # Output layer with a single unit and sigmoid activation for binary classification
    tf.keras.layers.Dense(1, activation='sigmoid')
])
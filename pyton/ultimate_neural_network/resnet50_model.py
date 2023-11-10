import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam

# Load the pre-trained ResNet50 model
base_model = ResNet50(weights='imagenet', include_top=False)

# Freeze the layers of the base model
for layer in base_model.layers:
    layer.trainable = False

# Add new layers for our specific task
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

# Load and preprocess the dataset
train_datagen = ImageDataGenerator(preprocessing_function=preprocess_input, 
                                   rotation_range=30, width_shift_range=0.2, 
                                   height_shift_range=0.2, shear_range=0.2, 
                                   zoom_range=0.2, horizontal_flip=True, 
                                   fill_mode='nearest')

test_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

train_generator = train_datagen.flow_from_directory(
    'path_to_train_data',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
    'path_to_validation_data',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical')

# Train the model
model.fit(train_generator, steps_per_epoch=train_generator.n//train_generator.batch_size, 
          epochs=10, validation_data=validation_generator, 
          validation_steps=validation_generator.n//validation_generator.batch_size)

# Save the model
model.save('ad_recognition_model.h5')

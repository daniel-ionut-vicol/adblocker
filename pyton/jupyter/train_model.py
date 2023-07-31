import tensorflow as tf
import os
# model building 
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
# evaluating performance 
from tensorflow.keras.metrics import Precision, Recall, BinaryAccuracy
# saving the model
from tensorflow.keras.models import load_model

# -------------------------------------------------------

# import the data
data = tf.keras.utils.image_dataset_from_directory("../processedDataSetAds/train")
data_iterator = data.as_numpy_iterator()
batch = data_iterator.next()

# scaling the data (normalizing)
data = data.map(lambda x, y: (x/255, y))

# split the data into train, val, and test
train_size = int(len(data)*.7)
val_size = int(len(data)*.2)+1
test_size = int(len(data)*.1)+1

# take the batches for each stage
train = data.take(train_size)
val = data.skip(train_size).take(val_size)
test = data.skip(train_size+val_size).take(test_size)

# building the model
model = Sequential()

model.add(Conv2D(16, (3,3), 1, activation='relu', input_shape=(256, 256, 3)))
model.add(MaxPooling2D())

model.add(Conv2D(32, (3,3), 1, activation='relu'))
model.add(MaxPooling2D())

model.add(Conv2D(16, (3,3), 1, activation='relu'))
model.add(MaxPooling2D())

model.add(Flatten())

model.add(Dense(256, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile('adam', loss=tf.losses.BinaryCrossentropy(), metrics=['accuracy'])

# train
# setup the logs directory 
logdir='logs'
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)

# hist contains data about the training
hist = model.fit(train, epochs=20, validation_data=val, callbacks=[tensorboard_callback])

# evaluate performance 
precision = Precision()
recall = Recall()
accuracy = BinaryAccuracy()

for batch in test.as_numpy_iterator():
    X, y = batch
    yhat = model.predict(X)
    precision.update_state(y, yhat)
    recall.update_state(y, yhat)
    accuracy.update_state(y, yhat)

print(f'Precision: {precision.result().numpy()}, Recall: {recall.result().numpy()}, Accuracy: {accuracy.result().numpy()}')

# saving the model
model.save(os.path.join('models', 'adnonadmodel.h5'))

#loading the model
# new_model = load_model(os.path.join('models', 'adnonadmodel.h5'))
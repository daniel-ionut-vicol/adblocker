import tensorflow as tf
import os
# model building 
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
# evaluating performance 
from tensorflow.keras.metrics import Precision, Recall, BinaryAccuracy
# loading the model
# from tensorflow.keras.models import load_model
# importing dataset
from get_dataset import DataSetLoader

# -------------------------------------------------------

# import the data
data_dirs = ["C:\\Users\\daniel2.DESKTOP-ARTCORE\\Documents\\AdVision\\adblocker\\pyton\\processedDataSetAds\\train\\0", "C:\\Users\\daniel2.DESKTOP-ARTCORE\\Documents\\AdVision\\adblocker\\pyton\\processedDataSetAds\\train\\1"]

dataset_loader = DataSetLoader()
datasets = []
for dir in data_dirs:
    datasets.append(dataset_loader.load(dir, label=os.path.basename(dir)))

full_dataset = datasets[0]

for dataset in datasets[0:]:
    full_dataset = full_dataset.concatenate(dataset)

shuffled_dataset = full_dataset.shuffle(buffer_size=1024) 

data_iterator = shuffled_dataset.as_numpy_iterator()
batch = data_iterator.next()

# scaling the data (normalizing)
normalized_data = shuffled_dataset.map(lambda x, y: (x/255, y))

# split the normalized_data into train, val, and test
train_size = int(len(normalized_data)*.7)
val_size = int(len(normalized_data)*.2)+1
test_size = int(len(normalized_data)*.1)+1

# take the batches for each stage
train = normalized_data.take(train_size)
val = normalized_data.skip(train_size).take(val_size)
test = normalized_data.skip(train_size+val_size).take(test_size)

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
# model.save(os.path.join('models', 'adnonadmodel.h5'))

#loading the model
# new_model = load_model(os.path.join('models', 'adnonadmodel.h5'))
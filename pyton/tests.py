import os

# def list_files(startpath):
#     print("Start");
#     for root, dirs, files in os.walk(startpath):
#         print("1");
#         for file in files:
#             if file.endswith(".png"):
#                 print(os.path.join(root, file))

# list_files("D:/work/aplicatii develbox/adblocker/pyton/fcn/dataset/")

import tensorflow as tf

from tensorflow.python.keras import backend as K
from tensorflow.python.keras.layers import Input, Dense, Conv2D
input_tensor = Input(shape=(32, 32, 3))
x = Conv2D(32, (3, 3))(input_tensor)
print(K.learning_phase())

tf.config.list_physical_devices()
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
tf.config.list_physical_devices('GPU')
tf.test.gpu_device_name()

print(tf.__version__)


from ai_benchmark import AIBenchmark
results = AIBenchmark().run() 
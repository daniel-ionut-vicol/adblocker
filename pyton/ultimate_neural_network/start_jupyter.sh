#!/bin/bash

docker run --gpus all -p 8080:8888 -v ~/jupyter:/tf  -v ~/dataset:/tf/dataset -v ~/cnn_training/models:/tf/models -it ad-detection-cnn-jupyter
#!/bin/bash

docker run --gpus all -v ~/dataset/:/app/dataset -v ~/cnn_training/models:/app/models -it ad-detection-cnn
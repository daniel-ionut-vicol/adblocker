#!/bin/bash

docker run --gpus all -v ~/Documents/adblocker/data/:/app/dataset -v ~/cnn_training/models:/app/models -it ad-detection-cnn
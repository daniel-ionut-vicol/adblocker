#!/bin/bash

# Step 4: start the docker image with a specific command
docker run --gpus all -v ~/Documents/adblocker/data/:/app/dataset -v ~/cnn_training/models:/app/models -it ad-detection-cnn
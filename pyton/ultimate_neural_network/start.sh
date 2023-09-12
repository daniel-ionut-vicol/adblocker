#!/bin/bash

# Step 4: start the docker image with a specific command
docker run --gpus all -v /home/mlserver/Documents/adblocker/data/:/app/dataset -v /home/mlserver/cnn_training/models:/app/models -it ad-detection-cnn
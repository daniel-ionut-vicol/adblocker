#!/bin/bash

# Step 1: git pull with your github credentials
git -c http.extraheader="AUTHORIZATION: bearer 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" pull origin master

# Replace <TOKEN> with your actual GitHub personal access token

# Step 2: remove the current container image with a specific name
docker rm -f ad-detection-cnn || true # Replace <CONTAINER_NAME> with your actual container name
docker rmi -f ad-detection-cnn || true # Replace <IMAGE_NAME> with your actual image name

# Step 3: build the docker image from current folder docker file
docker build -t ad-detection-cnn . # Replace <IMAGE_NAME> with your desired image name

# Step 4: start the docker image with a specific command
docker run --gpus all -v /home/mlserver/Documents/adblocker/data/:/app/dataset -v /home/mlserver/cnn_training/models:/app/models -it ad-detection-cnn
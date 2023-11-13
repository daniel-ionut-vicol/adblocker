#!/bin/bash

# Step 1: remove the current container image with a specific name
docker rm -f ad-detection-cnn || true
docker rmi -f ad-detection-cnn || true

# Step 2: build the docker image from current folder docker file
docker build -t ad-detection-cnn .
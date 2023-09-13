#!/bin/bash

# Set Git to use the credential memory cache
git config --global credential.helper cache

# Set the cache to timeout after 1 hour (setting is in seconds)
git config --global credential.helper 'cache --timeout=3600'

# Add your GitHub username and password/PAT to the Git configuration
# TODO: Find another way to authenticate, this is unsecure
git config --global user.name "RocketChamp"
git config --global user.password "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"

# Replace <TOKEN> with your actual GitHub personal access token

# Step 2: remove the current container image with a specific name
docker rm -f ad-detection-cnn || true # Replace <CONTAINER_NAME> with your actual container name
docker rmi -f ad-detection-cnn || true # Replace <IMAGE_NAME> with your actual image name

# Step 3: build the docker image from current folder docker file
docker build -t ad-detection-cnn . # Replace <IMAGE_NAME> with your desired image name
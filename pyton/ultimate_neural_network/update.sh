#!/bin/bash

# Set Git to use the credential memory cache with a timeout
git config --global credential.helper 'cache --timeout=3600'

# Replace <TOKEN> with your actual GitHub personal access token
echo "https://RocketChamp:<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>@github.com" > ~/.git-credentials

# Secure your ~/.git-credentials file
chmod 600 ~/.git-credentials

# Pull the latest code from the Git repository
git pull

# Step 2: remove the current container image with a specific name
docker rm -f ad-detection-cnn || true # Replace <CONTAINER_NAME> with your actual container name
docker rmi -f ad-detection-cnn || true # Replace <IMAGE_NAME> with your actual image name

# Step 3: build the docker image from current folder docker file
docker build -t ad-detection-cnn . # Replace <IMAGE_NAME> with your desired image name
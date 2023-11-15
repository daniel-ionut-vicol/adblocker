#!/bin/bash

# Prompt for environment variables
read -p "Enter image size (default 224): " IMAGE_SIZE
IMAGE_SIZE=${IMAGE_SIZE:-224}

read -p "Enter batch size (default 32): " BATCH_SIZE
BATCH_SIZE=${BATCH_SIZE:-32}

read -p "Enter epochs (default 10): " EPOCHS
EPOCHS=${EPOCHS:-10}

read -p "Enter patience (default 20): " PATIENCE
PATIENCE=${PATIENCE:-20}

read -p "Enter dataset path (default /app/dataset): " DATASET_PATH
DATASET_PATH=${DATASET_PATH:-/app/dataset}

read -p "Enter verbosity level (default 1): " VERBOSE_LEVEL
VERBOSE_LEVEL=${VERBOSE_LEVEL:-1}

read -p "Enter text input size (default 1): " TEXT_INPUT_SIZE
TEXT_INPUT_SIZE=${TEXT_INPUT_SIZE:-1}

# Run the Docker command
docker run --gpus all -v ~/dataset/:/app/dataset -v ~/cnn_training/models:/app/models -it -e IMAGE_SIZE=$IMAGE_SIZE -e BATCH_SIZE=$BATCH_SIZE -e EPOCHS=$EPOCHS -e PATIENCE=$PATIENCE -e DATASET_PATH=$DATASET_PATH -e VERBOSE_LEVEL=$VERBOSE_LEVEL -e TEXT_INPUT_SIZE=$TEXT_INPUT_SIZE ad-detection-cnn

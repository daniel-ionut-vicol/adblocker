#!/bin/bash

# Define the base directory
BASE_DIR="/mnt/data/mlserver/adblock/pyton/ultimate_neural_network"

# Activate the virtual environment
source "${BASE_DIR}/virtenv/bin/activate"

# Export the DATA environment variable
export DATA="/mnt/data/mlserver"

# Get the model path from the command-line arguments
MODEL_PATH=$DATA/cnn_training/$1

# Extract the model folder name and the model file name from the model path
MODEL_FOLDER_NAME=$(basename "$(dirname "$(dirname "$MODEL_PATH")")")
MODEL_FILE_NAME=$(basename "$MODEL_PATH" .h5)  # Remove the .h5 extension

# Define the output directory
OUTPUT_DIR="/mnt/data/mlserver/adblock/pyton/flask_backend/model_server/${MODEL_FOLDER_NAME}${MODEL_FILE_NAME}"

# Create the output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Change to the directory where the script is located
cd "${BASE_DIR}/automation"

# Start the evaluation in the background, redirecting stdout and stderr to a log file
nohup tensorflowjs_converter --input_format=keras "$MODEL_PATH" "$OUTPUT_DIR" > convert.log 2>&1 &

#!/bin/bash

# Define the base directory
BASE_DIR="/mnt/data/mlserver/adblock/pyton/ultimate_neural_network"

# Activate the virtual environment
source "${BASE_DIR}/virtenv/bin/activate"

# Export the DATA environment variable
export DATA="/mnt/data/mlserver"

# Get the model path from the command-line arguments
MODEL_PATH=$1

# Change to the directory where the script is located
cd "${BASE_DIR}/training"

# Start the evaluation in the background, redirecting stdout and stderr to a log file
nohup python3 evaluate.py "${MODEL_PATH}" > "${BASE_DIR}/last_evaluation.log" 2>&1 &

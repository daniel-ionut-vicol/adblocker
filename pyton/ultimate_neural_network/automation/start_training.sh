#!/bin/bash

# Define the base directory
BASE_DIR="/mnt/data/mlserver/adblock/pyton/ultimate_neural_network"

# Activate the virtual environment
source "${BASE_DIR}/virtenv/bin/activate"

# Export the DATA environment variable
export DATA="/mnt/data/mlserver"

# Change to the directory where the script is located
cd "${BASE_DIR}/training"

# Start the training in the background, redirecting stdout and stderr to a log file
nohup python3 "${BASE_DIR}/training/resnet50_training.py" > "${BASE_DIR}/last_training.log" 2>&1 &


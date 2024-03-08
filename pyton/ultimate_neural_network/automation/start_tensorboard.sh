#!/bin/bash

source /mnt/data/mlserver/adblock/pyton/ultimate_neural_network/virtenv/bin/activate
# Export the DATA environment variable
export DATA="/mnt/data/mlserver"

# Get the model path from the command-line arguments
LOGDIR=$DATA/cnn_training/$1

# Extract the model folder name and the model file name from the model path
MODEL_FOLDER_NAME=$(basename "$(dirname "$LOGDIR")")

nohup tensorboard --logdir $LOGDIR --host 0.0.0.0 > $DATA/cnn_training/models/$MODEL_FOLDER_NAME/tensorboard.log 2>&1 &
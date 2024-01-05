#!/bin/bash

docker run --gpus all -p 8080:8888 -e JUPYTER_ENABLE_LAB=yes -e TF_FORCE_GPU_ALLOW_GROWTH=true -v $DATA/jupyter:/tf/jupyter -v $DATA/adblock/pyton/ultimate_neural_network:/tf/project  -v $DATA/dataset:/home/dataset -v $DATA/cnn_training/models:/home/models -it ad-detection-cnn-jupyter jupyter notebook --ip 0.0.0.0 --no-browser --allow-root --debug

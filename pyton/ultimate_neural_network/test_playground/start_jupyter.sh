#!/bin/bash

docker run --gpus all -p 8080:8888 -v ~/jupyter:/tf/jupyter -v ~/adblock/pyton/ultimate_neural_network:/tf/project  -v ~/newdataset:/tf/dataset -v ~/cnn_training/models:/tf/models -it ad-detection-cnn-jupyter

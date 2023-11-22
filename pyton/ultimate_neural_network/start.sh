#!/bin/bash

# Default values
IMAGE_SIZE=224
BATCH_SIZE=32
EPOCHS=10
PATIENCE=20
DATASET_PATH=/app/dataset
VERBOSE_LEVEL=1
TEXT_INPUT_SIZE=1

# A function to display a help message
show_help() {
	echo "Usage: $0 [options...]"
	echo
	echo "Options:"
	echo " -i, --image_size       Set the image size (default: $IMAGE_SIZE)"
	echo " -b, --batch_size       Set the batch size (default: $BATCH_SIZE)"
	echo " -e, --epochs           Set the number of epochs (default: $EPOCHS)"
	echo " -p, --patience         Set the patience (default: $PATIENCE)"
	echo " -d, --dataset_path     Set the dataset path (default: $DATASET_PATH)"
	echo " -v, --verbose_level    Set the verbosity level (default: $VERBOSE_LEVEL)"
	echo " -t, --text_input_size  Set the text input size (default: $TEXT_INPUT_SIZE)"
	echo " -h, --help             Display this help message"
}

# Parse command-line arguments
OPTIONS=$(getopt -o i:b:e:p:d:v:t:h --long image_size:,batch_size:,epochs:,patience:,dataset_path:,verbose_level:,text_input_size:,help -n "$0" -- "$@")
eval set -- "$OPTIONS"

while true; do
	case "$1" in
	-i | --image_size)
		IMAGE_SIZE=$2
		shift 2
		;;
	-b | --batch_size)
		BATCH_SIZE=$2
		shift 2
		;;
	-e | --epochs)
		EPOCHS=$2
		shift 2
		;;
	-p | --patience)
		PATIENCE=$2
		shift 2
		;;
	-d | --dataset_path)
		DATASET_PATH=$2
		shift 2
		;;
	-v | --verbose_level)
		VERBOSE_LEVEL=$2
		shift 2
		;;
	-t | --text_input_size)
		TEXT_INPUT_SIZE=$2
		shift 2
		;;
	-h | --help)
		show_help
		exit 0
		shift
		;;
	--)
		shift
		break
		;;
	*)
		echo "Internal error!"
		exit 1
		;;
	esac
done

# Run the Docker command
docker run --gpus all -v ~/adblock/pyton/ultimate_neural_network:/app -v ~/dataset:/home/dataset -v ~/cnn_training/models:/home/models -it -e IMAGE_SIZE=$IMAGE_SIZE -e BATCH_SIZE=$BATCH_SIZE -e EPOCHS=$EPOCHS -e PATIENCE=$PATIENCE -e DATASET_PATH=$DATASET_PATH -e VERBOSE_LEVEL=$VERBOSE_LEVEL -e TEXT_INPUT_SIZE=$TEXT_INPUT_SIZE ad-detection-cnn

import os
import json

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Use the script directory to construct the absolute path to config.json
config_path = os.path.join(script_dir, 'config.json')

# Load the configuration data from config.json
with open(config_path) as f:
    config = json.load(f)

WORK_DIR = os.environ.get("WORK_DIR", config.get("WORK_DIR", "/tf/project"))
MODEL = os.environ.get("MODEL", config.get("MODEL", "RESNET50"))
IMAGE_SIZE = int(os.environ.get("IMAGE_SIZE", config.get("IMAGE_SIZE", 224)))
AD_IMAGE_LIMIT = os.environ.get("AD_IMAGE_LIMIT", config.get("AD_IMAGE_LIMIT", "all"))
NONAD_IMAGE_LIMIT = os.environ.get("NONAD_IMAGE_LIMIT", config.get("NONAD_IMAGE_LIMIT", "all"))
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", config.get("BATCH_SIZE", 16)))
EPOCHS = int(os.environ.get("EPOCHS", config.get("EPOCHS", 100)))
PATIENCE = int(os.environ.get("PATIENCE", config.get("PATIENCE", 20)))
VERBOSE_LEVEL = int(os.environ.get("VERBOSE_LEVEL", config.get("VERBOSE_LEVEL", 1)))
DATASET_PATH = os.environ.get("DATASET_PATH", config.get("DATASET_PATH", f"{os.environ['DATA']}/newdataset"))
TRAIN_RATIO = float(os.environ.get("TRAIN_RATIO", config.get("TRAIN_RATIO", 0.6)))
VAL_RATIO = float(os.environ.get("VAL_RATIO", config.get("VAL_RATIO", 0.2)))
TEST_RATIO = float(os.environ.get("TEST_RATIO", config.get("TEST_RATIO", 0.2)))
# Load ImageDataGenerator parameters
USE_AUGMENTATION = str(config.get("USE_AUGMENTATION", "false")).lower() == "true"
ROTATION_RANGE = int(config.get("ROTATION_RANGE", 20))
WIDTH_SHIFT_RANGE = float(config.get("WIDTH_SHIFT_RANGE", 0.2))
HEIGHT_SHIFT_RANGE = float(config.get("HEIGHT_SHIFT_RANGE", 0.2))
BRIGHTNESS_RANGE = list(map(float, config.get("BRIGHTNESS_RANGE", "0.8,1.2").split(',')))
HORIZONTAL_FLIP = str(config.get("HORIZONTAL_FLIP", "true")).lower() == "true"
FILL_MODE = str(config.get("FILL_MODE", "nearest"))
RESCALE_NUMERATOR = float(config.get("RESCALE_NUMERATOR", 1.0))
RESCALE_DENOMINATOR = float(config.get("RESCALE_DENOMINATOR", 255))
RESCALE = RESCALE_NUMERATOR / RESCALE_DENOMINATOR

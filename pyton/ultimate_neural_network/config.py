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
IMAGE_SIZE = int(os.environ.get("IMAGE_SIZE", config.get("IMAGE_SIZE", 224)))
AD_IMAGE_LIMIT = os.environ.get("AD_IMAGE_LIMIT", config.get("AD_IMAGE_LIMIT", "all"))
NONAD_IMAGE_LIMIT = os.environ.get("NONAD_IMAGE_LIMIT", config.get("NONAD_IMAGE_LIMIT", "all"))
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", config.get("BATCH_SIZE", 16)))
EPOCHS = int(os.environ.get("EPOCHS", config.get("EPOCHS", 100)))
PATIENCE = int(os.environ.get("PATIENCE", config.get("PATIENCE", 20)))
DATASET_PATH = os.environ.get("DATASET_PATH", config.get("DATASET_PATH", f"{os.environ['DATA']}/newdataset"))
VERBOSE_LEVEL = int(os.environ.get("VERBOSE_LEVEL", config.get("VERBOSE_LEVEL", 1)))

import os

WORK_DIR = os.environ.get("WORK_DIR", "/app")
IMAGE_SIZE = int(os.environ.get("IMAGE_SIZE", 224))
# TODO: Check if this works
AD_IMAGE_LIMIT = os.environ.get("AD_IMAGE_LIMIT", "all")
NONAD_IMAGE_LIMIT = os.environ.get("NONAD_IMAGE_LIMIT", "all")
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", 32))
EPOCHS = int(os.environ.get("EPOCHS", 10))
PATIENCE = int(os.environ.get("PATIENCE", 20))
DATASET_PATH = os.environ.get("DATASET_PATH", "/home/dataset")
VERBOSE_LEVEL = int(os.environ.get("VERBOSE_LEVEL", 1))
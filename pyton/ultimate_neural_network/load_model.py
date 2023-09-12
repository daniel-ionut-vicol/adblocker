from tensorflow.keras.models import load_model
from custom_metrics import precision, recall, f1_score

def load_model(model_path):
    return load_model(model_path, custom_objects={'precision': precision, "recall": recall, "f1_score": f1_score})
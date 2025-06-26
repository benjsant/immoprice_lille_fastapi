import os
import joblib

def load_model(filename: str):
    path = os.path.join("app", "models", filename)
    return joblib.load(path)
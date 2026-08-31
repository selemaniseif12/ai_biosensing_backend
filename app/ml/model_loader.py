# app/ml/model_loader.py

import joblib
import os

def load_model(model_path: str):
    """
    Loads a model from a given path with safety checks.

    Parameters:
        model_path (str): Path to the .pkl model file

    Returns:
        model: Loaded ML model
    """

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    model = joblib.load(model_path)
    return model


def load_v2_model():
    """
    Loads the 100-virus V2 model.
    Update the path if needed.
    """
    path = "app/ml/models/classify/v2/sim_model_v2_100.pkl"
    return load_model(path)


def load_v6_model():
    """
    Loads the 100-virus V6 model.
    Update the path if needed.
    """
    path = "app/ml/models/classify/v6/sim_model_v6_100.pkl"
    return load_model(path)


def load_spectral_model():
    """
    Loads the spectral FFT model.
    """
    path = "app/ml/models/classify/spectral/spectral_model.pkl"
    return load_model(path)

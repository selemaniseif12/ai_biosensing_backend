import os
import joblib
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "predict_models")

def load_rf_model():
    path = os.path.join(MODEL_DIR, "rf_model.pkl")
    return joblib.load(path)

def load_scaler():
    path = os.path.join(MODEL_DIR, "scaler.pkl")
    return joblib.load(path)

def predict(features: list):
    model = load_rf_model()
    scaler = load_scaler()

    X = np.array(features).reshape(1, -1)
    X_scaled = scaler.transform(X)

    prediction = model.predict(X_scaled)[0]
    return float(prediction)

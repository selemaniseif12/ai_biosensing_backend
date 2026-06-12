import os
import joblib
from tensorflow.keras.models import load_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PREDICT_MODELS_DIR = os.path.join(BASE_DIR, "predict_models")

def load_rf():
    path = os.path.join(PREDICT_MODELS_DIR, "rf_model.pkl")
    return joblib.load(path)

def load_xgboost():
    path = os.path.join(PREDICT_MODELS_DIR, "xgb_model.pkl")
    return joblib.load(path)

def load_lstm():
    model_path = os.path.join(PREDICT_MODELS_DIR, "lstm_model.h5")
    scaler_path = os.path.join(PREDICT_MODELS_DIR, "lstm_scaler.pkl")
    model = load_model(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

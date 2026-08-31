from fastapi import APIRouter
import joblib
import numpy as np
import pandas as pd
from pydantic import BaseModel

MODEL_PATH = "app/models/virus_multiclassify_V7_175_prob.pkl"
model = joblib.load(MODEL_PATH)

router = APIRouter(prefix="/virus", tags=["Virus Multiclass"])

BASE_F = 1693999.6834565601

CSV_PATH = "app/models/data/virus_multiclass.csv"
virus_table = pd.read_csv(CSV_PATH)
virus_table.columns = virus_table.columns.str.strip().str.lower()

virus_id_col = "virus_id"
mass_col = "mass_fg"

mass_map = dict(
    zip(
        virus_table[virus_id_col].astype(str),
        virus_table[mass_col]
    )
)

def compute_sensor_offset(measured_frequency_hz: float):
    return measured_frequency_hz - BASE_F

class VirusInput(BaseModel):
    mass_fg: float
    frequency_hz: float
    deposition_rate_s: float
    temperature_c: float
    humidity_pct: float
    flow_rate: float
    time_to_detection_s: float
    antibody: float
    antigen: float

def clean_predictions(raw_ids, pred_prob):
    clean_ids = []
    clean_probs = []
    for cls, prob in zip(raw_ids, pred_prob):
        cls_str = str(cls)
        try:
            prob_float = float(prob)
        except:
            continue
        clean_ids.append(cls_str)
        clean_probs.append(prob_float)
    return clean_ids, clean_probs

@router.post("/dashboard_data")
def dashboard_data():
    synthetic_frequency_hz = BASE_F + 0.05
    sensor_offset = compute_sensor_offset(synthetic_frequency_hz)
    frequency_mhz = synthetic_frequency_hz / 1_000_000

    X = pd.DataFrame([{
        "mass_fg": 0.00018,
        "frequency_mhz": frequency_mhz,
        "deposition_rate_s": 0.35,
        "temperature_c": 23,
        "humidity_pct": 20,
        "flow_rate": 1.5,
        "time_to_detection_s": 16,
        "antibody": "0.8",
        "antigen": "0.6"
    }])

    pred_prob = model.predict_proba(X)[0]
    raw_ids = model.classes_
    clean_ids, clean_probs = clean_predictions(raw_ids, pred_prob)

    mass_fg = [mass_map.get(vid, None) for vid in clean_ids]

    return {
        "model_version": "Virus Multiclass V7-175 (probabilities)",
        "virus_ids": clean_ids,
        "probabilities": clean_probs,
        "mass_fg": mass_fg,
        "sensor_frequency_offset": sensor_offset,
        "measured_frequency_hz": synthetic_frequency_hz
    }

@router.post("/probabilities/v7")
def v7_probabilities(payload: VirusInput):
    frequency_mhz = payload.frequency_hz / 1_000_000
    sensor_offset = compute_sensor_offset(payload.frequency_hz)

    X = pd.DataFrame([{
        "mass_fg": payload.mass_fg,
        "frequency_mhz": frequency_mhz,
        "deposition_rate_s": payload.deposition_rate_s,
        "temperature_c": payload.temperature_c,
        "humidity_pct": payload.humidity_pct,
        "flow_rate": payload.flow_rate,
        "time_to_detection_s": payload.time_to_detection_s,
        "antibody": str(payload.antibody),
        "antigen": str(payload.antigen)
    }])

    pred_prob = model.predict_proba(X)[0]
    raw_ids = model.classes_
    clean_ids, clean_probs = clean_predictions(raw_ids, pred_prob)

    top_indices = np.argsort(clean_probs)[::-1][:5]
    top_predictions = [
        {"virus_id": clean_ids[i], "probability": clean_probs[i]}
        for i in top_indices
    ]

    return {
        "model_version": "Virus Multiclass V7-175 (probabilities)",
        "virus_ids": clean_ids,
        "probabilities": clean_probs,
        "top_predictions": top_predictions,
        "sensor_frequency_offset": sensor_offset,
        "measured_frequency_hz": payload.frequency_hz
    }

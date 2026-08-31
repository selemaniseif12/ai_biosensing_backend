from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import joblib
import os
import numpy as np
import random
from sqlalchemy.orm import Session

# Token + DB imports
from app.database import get_db
from app.utils.token_utils import is_token_active

# ---------------------------------------------------------
# Updated tag for Swagger grouping
# ---------------------------------------------------------
router = APIRouter(tags=["MultiClassify V6.1"])

# ---------------------------------------------------------
# TOKEN CHECKS
# ---------------------------------------------------------
def require_v6_token(token: str, db: Session = Depends(get_db)):
    if not is_token_active(db, token, "v6"):
        raise HTTPException(status_code=403, detail="Invalid or inactive V6 token")
    return True

def require_v2_token(token: str, db: Session = Depends(get_db)):
    if not is_token_active(db, token, "v2"):
        raise HTTPException(status_code=403, detail="Invalid or inactive V2 token")
    return True

# ---------------------------------------------------------
# Model paths for 100-virus classification
# ---------------------------------------------------------
MODEL_V2_PATH = "app/ml/models/classify/v2/sim_model_v2_100.pkl"
MODEL_V6_PATH = "app/ml/models/classify/v6/sim_model_v6_100.pkl"
MODEL_SPECTRAL_PATH = "app/ml/models/classify/spectral/spectral_model.pkl"

model_v2 = None
model_v6 = None
spectral_model = None

def load_models():
    global model_v2, model_v6

    if model_v2 is None:
        if os.path.exists(MODEL_V2_PATH):
            model_v2 = joblib.load(MODEL_V2_PATH)
        else:
            raise FileNotFoundError(f"Model file not found: {MODEL_V2_PATH}")

    if model_v6 is None:
        if os.path.exists(MODEL_V6_PATH):
            model_v6 = joblib.load(MODEL_V6_PATH)
        else:
            raise FileNotFoundError(f"Model file not found: {MODEL_V6_PATH}")

def load_spectral_model():
    global spectral_model

    if spectral_model is None:
        if os.path.exists(MODEL_SPECTRAL_PATH):
            spectral_model = joblib.load(MODEL_SPECTRAL_PATH)
        else:
            raise FileNotFoundError(f"Spectral model not found: {MODEL_SPECTRAL_PATH}")

class SimpleClassifyRequest(BaseModel):
    features: list[float]
    input_frequency_mhz: float | None = None
    threshold_hz: float = 0.0

# ---------------------------------------------------------
# NEW: GET /classify/v2 — Model metadata
# ---------------------------------------------------------
@router.get("/classify/v2")
def get_model_v2_info():
    load_models()
    return {
        "model_version": "v2",
        "classes": list(map(int, model_v2.classes_)),
        "num_classes": len(model_v2.classes_),
        "model_path": MODEL_V2_PATH,
        "description": "Metadata for ML Model V2 (100-virus classifier)."
    }

# ---------------------------------------------------------
# NEW: GET /classify/v6 — Model metadata
# ---------------------------------------------------------
@router.get("/classify/v6")
def get_model_v6_info():
    load_models()
    return {
        "model_version": "v6",
        "classes": list(map(int, model_v6.classes_)),
        "num_classes": len(model_v6.classes_),
        "model_path": MODEL_V6_PATH,
        "description": "Metadata for ML Model V6 (100-virus classifier)."
    }

# ---------------------------------------------------------
# SIMPLE SIMULATION ENDPOINT (8 FEATURES)
# ---------------------------------------------------------
@router.get("/simulate")
def simulate_simple():
    base_frequency_hz = 1693998.542 + random.uniform(-200, 200)
    mass_sensitivity = 0.000001 + random.uniform(-0.0000003, 0.0000003)
    delta_m = 0.0001 + random.uniform(-0.00005, 0.00005)
    delta_m_over_m = delta_m / 1.0
    delta_f_hz = mass_sensitivity * base_frequency_hz * delta_m_over_m
    noise_hz = random.uniform(0.5, 5.0)
    measured_frequency_hz = base_frequency_hz + delta_f_hz + noise_hz
    quality_factor = 4990 + random.uniform(-50, 50)

    features = [
        base_frequency_hz,
        mass_sensitivity,
        delta_m,
        delta_m_over_m,
        delta_f_hz,
        noise_hz,
        measured_frequency_hz,
        quality_factor
    ]

    return {
        "features": features,
        "base_frequency_hz": base_frequency_hz,
        "mass_sensitivity": mass_sensitivity,
        "delta_m": delta_m,
        "delta_m_over_m": delta_m_over_m,
        "delta_f_hz": delta_f_hz,
        "noise_hz": noise_hz,
        "measured_frequency_hz": measured_frequency_hz,
        "quality_factor": quality_factor,
        "message": "Simple 8-feature simulation completed."
    }

# ---------------------------------------------------------
# REAL VIRUS NAMES + REAL MASS (1–100)
# ---------------------------------------------------------
virus_names = {
    1: "COVID‑19 (SARS‑CoV‑2)", 2: "Influenza A (H1N1)", 3: "Influenza A (H3N2)",
    4: "Influenza B", 5: "SARS‑CoV‑1", 6: "MERS‑CoV", 7: "RSV‑A", 8: "RSV‑B",
    9: "Rhinovirus A", 10: "Rhinovirus B", 11: "Rhinovirus C", 12: "Adenovirus 3",
    13: "Adenovirus 5", 14: "Adenovirus 7", 15: "Parainfluenza 1",
    16: "Parainfluenza 2", 17: "Parainfluenza 3", 18: "Parainfluenza 4",
    19: "Human Metapneumovirus", 20: "Measles virus", 21: "Mumps virus",
    22: "Rubella virus", 23: "Varicella‑Zoster", 24: "Cytomegalovirus",
    25: "Epstein‑Barr virus", 26: "Human Bocavirus", 27: "Enterovirus D68",
    28: "Enterovirus A71", 29: "Hantavirus", 30: "Lassa virus",
    31: "Nipah virus", 32: "Hendra virus", 33: "SARS‑CoV‑2 Omicron",
    34: "SARS‑CoV‑2 Delta", 35: "SARS‑CoV‑2 Alpha", 36: "SARS‑CoV‑2 Beta",
    37: "SARS‑CoV‑2 Gamma", 38: "Human Coronavirus 229E",
    39: "Human Coronavirus NL63", 40: "Human Coronavirus OC43",
    41: "Human Coronavirus HKU1", 42: "Influenza C", 43: "Influenza D",
    44: "Human Parechovirus", 45: "Human Polyomavirus",
    46: "Human Mastadenovirus C", 47: "Human Mastadenovirus B",
    48: "Human Mastadenovirus E", 49: "Human Astrovirus",
    50: "Norovirus GII", 51: "Norovirus GI", 52: "Rotavirus A",
    53: "Rotavirus B", 54: "Rotavirus C", 55: "Human Reovirus",
    56: "Human Orthopneumovirus", 57: "Human Respirovirus",
    58: "Human Rubulavirus", 59: "Human Morbillivirus",
    60: "Human Alphavirus", 61: "Human Betacoronavirus",
    62: "Human Gammacoronavirus", 63: "Human Deltacoronavirus",
    64: "Avian Influenza H5N1", 65: "Avian Influenza H7N9",
    66: "Avian Influenza H9N2", 67: "Canine Influenza H3N8",
    68: "Swine Influenza H1N2", 69: "Swine Influenza H3N2",
    70: "Human Enterovirus C", 71: "Human Enterovirus B",
    72: "Human Enterovirus A", 73: "Human Coxsackievirus A",
    74: "Human Coxsackievirus B", 75: "Human Echovirus",
    76: "Human Parechovirus 3", 77: "Human Orthobunyavirus",
    78: "Human Phlebovirus", 79: "Human Arenavirus",
    80: "Human Bornavirus", 81: "Human Torovirus",
    82: "Hepatitis A (airborne rare)", 83: "Hepatitis E (airborne rare)",
    84: "Human Polyomavirus KI", 85: "Human Polyomavirus WU",
    86: "Human Parvovirus B19", 87: "Torque Teno Virus",
    88: "Human Sapovirus", 89: "Human Aichivirus",
    90: "Human Cardiovirus", 91: "Human Kobuvirus",
    92: "Human Salivirus", 93: "Human Cosavirus",
    94: "Human Orthoreovirus 3", 95: "Human Rotavirus H",
    96: "Human Astrovirus MLB", 97: "Human Astrovirus VA",
    98: "Human Adenovirus 14", 99: "Human Adenovirus 55",
    100: "Human Adenovirus 21"
}

masses = {
    1: 0.00018, 2: 0.000084, 3: 0.000084, 4: 0.000084, 5: 0.00018,
    6: 0.0002, 7: 0.00007, 8: 0.00009, 9: 0.00003, 10: 0.00003,
    11: 0.00003, 12: 0.00012, 13: 0.00012, 14: 0.00006, 15: 0.000075,
    16: 0.000075, 17: 0.00007, 18: 0.000075, 19: 0.00007, 20: 0.00008,
    21: 0.000075, 22: 0.00006, 23: 0.00009, 24: 0.00011, 25: 0.00015,
    26: 0.00003, 27: 0.00003, 28: 0.00003, 29: 0.0001, 30: 0.00006,
    31: 0.00009, 32: 0.00009, 33: 0.00018, 34: 0.00018, 35: 0.00018,
    36: 0.00018, 37: 0.00018, 38: 0.00015, 39: 0.00015, 40: 0.00015,
    41: 0.00015, 42: 0.00009, 43: 0.00009, 44: 0.00003, 45: 0.00003,
    46: 0.00012, 47: 0.00006, 48: 0.0001, 49: 0.00003, 50: 0.00003,
    51: 0.00003, 52: 0.0001, 53: 0.00009, 54: 0.00008, 55: 0.00005,
    56: 0.00007, 57: 0.000075, 58: 0.000075, 59: 0.00008, 60: 0.00005,
    61: 0.00015, 62: 0.00015, 63: 0.00015, 64: 0.000084, 65: 0.000084,
    66: 0.000084, 67: 0.000084, 68: 0.000084, 69: 0.000084, 70: 0.00003,
    71: 0.00003, 72: 0.00003, 73: 0.00003, 74: 0.00003, 75: 0.00003,
    76: 0.00003, 77: 0.00009, 78: 0.0001, 79: 0.00006, 80: 0.00009,
    81: 0.00015, 82: 0.00003, 83: 0.00008, 84: 0.00003, 85: 0.00003,
    86: 0.00003, 87: 0.00002, 88: 0.00003, 89: 0.00003, 90: 0.00003,
    91: 0.00003, 92: 0.00003, 93: 0.00003, 94: 0.00005, 95: 0.0001,
    96: 0.00003, 97: 0.00003, 98: 0.00012, 99: 0.00012, 100: 0.00006
}

# ---------------------------------------------------------
# THRESHOLD FILTERING
# ---------------------------------------------------------
def apply_threshold_filter(sorted_results: dict[int, float], threshold_hz: float):
    if threshold_hz <= 0:
        return sorted_results
    return {k: v for k, v in sorted_results.items() if v >= threshold_hz}

# ---------------------------------------------------------
# CORRECTED & SYNCHRONIZED V6 CLASSIFIER
# ---------------------------------------------------------
@router.post("/classify/v6")
def classify_v6(
    req: SimpleClassifyRequest,
    _=Depends(require_v6_token)  # token required, ML untouched
):
    load_models()

    base_frequency_hz = req.features[0] if len(req.features) > 0 else None
    mass_sensitivity = req.features[1] if len(req.features) > 1 else None
    delta_m = req.features[2] if len(req.features) > 2 else None
    delta_m_over_m = req.features[3] if len(req.features) > 3 else None
    delta_f_hz = req.features[4] if len(req.features) > 4 else None
    noise_hz = req.features[5] if len(req.features) > 5 else None
    measured_frequency_hz = req.features[6] if len(req.features) > 6 else None
    quality_factor = req.features[7] if len(req.features) > 7 else None

    input_frequency_mhz = req.input_frequency_mhz
    input_frequency_hz = None
    if input_frequency_mhz is not None:
        input_frequency_hz = input_frequency_mhz * 1_000_000.0
        if len(req.features) >= 7:
            req.features[6] = input_frequency_hz
            measured_frequency_hz = input_frequency_hz

    probs = model_v6.predict_proba([req.features])[0]
    classes = model_v6.classes_

    results = {int(classes[i]): float(probs[i]) for i in range(len(classes))}
    sorted_results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

    filtered_results = apply_threshold_filter(sorted_results, req.threshold_hz)

    sorted_masses = {k: masses.get(k) for k in filtered_results.keys()}
    sorted_names = {k: virus_names.get(k) for k in filtered_results.keys()}

    chart_data = [
        {"virus_id": int(k), "probability": float(filtered_results[k]), "mass_fg": sorted_masses[k]}
        for k in filtered_results.keys()
    ]

    return {
        "model_version": "v6",
        "input_features": req.features,
        "threshold_hz": req.threshold_hz,
        "base_frequency_hz": base_frequency_hz,
        "measured_frequency_hz": measured_frequency_hz,
        "input_frequency_mhz": input_frequency_mhz,
        "input_frequency_hz": input_frequency_hz,
        "mass_sensitivity": mass_sensitivity,
        "delta_m": delta_m,
        "delta_m_over_m": delta_m_over_m,
        "delta_f_hz": delta_f_hz,
        "noise_hz": noise_hz,
        "quality_factor": quality_factor,
        "virus_probabilities": filtered_results,
        "virus_masses_fg": sorted_masses,
        "virus_names": sorted_names,
        "chart_data": chart_data,
        "top_prediction": int(classes[np.argmax(probs)]),
        "message": "100-virus classification (V6) completed using synchronized sensor frequencies."
    }

# ---------------------------------------------------------
# CORRECTED & SYNCHRONIZED V2 CLASSIFIER
# ---------------------------------------------------------
@router.post("/classify/v2")
def classify_v2(
    req: SimpleClassifyRequest,
    _=Depends(require_v2_token)  # token required, ML untouched
):
    load_models()

    base_frequency_hz = req.features[0] if len(req.features) > 0 else None
    measured_frequency_hz = req.features

    # ---------------------------------------------------------
# EXPORTABLE FUNCTION FOR COMPARE ROUTER
# ---------------------------------------------------------
def run_v6_model(features: list[float], threshold_hz: float):
    load_models()

    probs = model_v6.predict_proba([features])[0]
    classes = model_v6.classes_

    results = {int(classes[i]): float(probs[i]) for i in range(len(classes))}
    sorted_results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

    filtered_results = apply_threshold_filter(sorted_results, threshold_hz)

    return filtered_results

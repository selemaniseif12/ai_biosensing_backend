from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import joblib
import numpy as np
import os
import shap
import matplotlib.pyplot as plt
import uuid

from app.dependencies.database import get_db
from app.crud.ml_logging import log_prediction

router = APIRouter()

# ---------------------------------------------------------
# Load model + encoder safely
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "qcm_virus_classifier_rf.joblib")
ENCODER_PATH = os.path.join(BASE_DIR, "models", "qcm_virus_label_encoder.joblib")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

if not os.path.exists(ENCODER_PATH):
    raise FileNotFoundError(f"Label encoder file not found: {ENCODER_PATH}")

model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)

# SHAP explainer
explainer = shap.TreeExplainer(model)

# Directory for SHAP force plots
FORCE_DIR = os.path.join(BASE_DIR, "models", "shap_force_plots")
os.makedirs(FORCE_DIR, exist_ok=True)

# ---------------------------------------------------------
# Input schema
# ---------------------------------------------------------
class QCMInput(BaseModel):
    device1: float = Field(..., description="Frequency shift from device 1")
    device2: float = Field(..., description="Frequency shift from device 2")
    device3: float = Field(..., description="Frequency shift from device 3")
    device4: float = Field(..., description="Frequency shift from device 4")
    device5: float = Field(..., description="Frequency shift from device 5")

# ---------------------------------------------------------
# Prediction endpoint with logging
# ---------------------------------------------------------
@router.post("/predict")
def predict_virus(data: QCMInput, db: Session = Depends(get_db)):
    try:
        # Prepare input
        features = np.array([
            data.device1,
            data.device2,
            data.device3,
            data.device4,
            data.device5
        ]).reshape(1, -1)

        # Predict class
        class_id = model.predict(features)[0]

        # Probability distribution
        probabilities = model.predict_proba(features)[0]
        confidence = float(np.max(probabilities))

        # Decode label
        virus_name = label_encoder.inverse_transform([class_id])[0]

        # Log prediction to database
        log_prediction(
            db=db,
            data=data,
            class_id=int(class_id),
            virus_name=virus_name,
            confidence=confidence
        )

        # Return response
        return {
            "predicted_class_id": int(class_id),
            "predicted_virus": virus_name,
            "confidence": confidence,
            "probabilities": {
                label_encoder.inverse_transform([i])[0]: float(probabilities[i])
                for i in range(len(probabilities))
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------------------------------------
# ⭐ NEW: SHAP EXPLAIN ENDPOINT
# ---------------------------------------------------------
@router.post("/explain")
def explain_virus(data: QCMInput):
    try:
        # Prepare input
        features = np.array([
            data.device1,
            data.device2,
            data.device3,
            data.device4,
            data.device5
        ]).reshape(1, -1)

        # SHAP values
        shap_values = explainer.shap_values(features)

        # Generate unique filename
        plot_id = str(uuid.uuid4())
        plot_path = os.path.join(FORCE_DIR, f"force_plot_{plot_id}.png")

        # Create SHAP force plot
        shap.force_plot(
            explainer.expected_value,
            shap_values[0],
            features[0],
            feature_names=["device1", "device2", "device3", "device4", "device5"],
            matplotlib=True
        )
        plt.savefig(plot_path, bbox_inches='tight')
        plt.close()

        # Predict virus
        class_id = model.predict(features)[0]
        virus_name = label_encoder.inverse_transform([class_id])[0]

        return {
            "predicted_virus": virus_name,
            "explanation_plot": plot_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

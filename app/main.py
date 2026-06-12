import logging.config
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

from app.core.logging_config import LOGGING_CONFIG

# Routers
from app.routers import auth, customers, samples, measurements
from app.routers import analyzer_v1, analyzer_v2, analyzer_v3, analyzer_v4
from app.routers import analyzer_v5, analyzer_v6
from app.routers.analysis import router as analysis_router
from app.routers.analyze_router import router as unified_analyze_router
from app.routers.admin_analytics_router import router as admin_analytics_router
from app.routers.orchestrator_router import router as orchestrator_router
from app.routers.ml_predict_router import router as ml_predict_router
from app.routers.ml_classify_router import router as ml_classify_router

from app.ml.model_loader import load_rf, load_xgboost, load_lstm
from app.initialize_database import initialize_database


app = FastAPI(
    title="AI Biosensing API",
    version="1.0.0",
    description="QCM biosensing platform with analyzers, ML pipeline, unified analysis, orchestrator, and admin analytics."
)

# ---------------------------------------------------------
# CORS FIX — this is what allows your frontend to connect
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logging.config.dictConfig(LOGGING_CONFIG)
    initialize_database()


# -------------------------
# Router Includes
# -------------------------

# Only ONE include for auth — this removes duplication
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

app.include_router(customers.router, prefix="/customers", tags=["Customers"])
app.include_router(samples.router, prefix="/samples", tags=["Samples"])
app.include_router(measurements.router, prefix="/measurements", tags=["Measurements"])

app.include_router(analyzer_v1.router, tags=["Analyzer v1"])
app.include_router(analyzer_v2.router, tags=["Analyzer v2"])
app.include_router(analyzer_v3.router, tags=["Analyzer v3"])
app.include_router(analyzer_v4.router, tags=["Analyzer v4"])
app.include_router(analyzer_v5.router, tags=["Analyzer v5"])
app.include_router(analyzer_v6.router, tags=["Analyzer v6"])

app.include_router(analysis_router, tags=["Analysis"])
app.include_router(unified_analyze_router, tags=["Unified Analyze"])
app.include_router(admin_analytics_router, tags=["Admin Analytics"])
app.include_router(orchestrator_router, tags=["Analyzer Orchestrator"])

app.include_router(ml_predict_router, tags=["ML Regression"])
app.include_router(ml_classify_router, tags=["ML Classification"])


# -------------------------
# Legacy ML Prediction
# -------------------------

class VirusData(BaseModel):
    ID: int
    virus: str
    device_id: str
    deposition_rate: float
    temperature: float
    humidity: float
    flow_rate: float
    time_to_detection: float
    mass_of_virus_fg: float
    required_virus_count: float


@app.post("/predict", tags=["ML Prediction"])
def predict(payload: VirusData, model_type: str = "rf"):
    device_num = int(payload.device_id.replace("Device-", "").replace("Device‑", ""))

    data = [
        payload.ID,
        device_num,
        payload.deposition_rate,
        payload.temperature,
        payload.humidity,
        payload.flow_rate,
        payload.mass_of_virus_fg,
        payload.required_virus_count,
    ]

    if model_type == "rf":
        model = load_rf()
        prediction = model.predict([data])[0]
    elif model_type == "xgb":
        model = load_xgboost()
        prediction = model.predict([data])[0]
    elif model_type == "lstm":
        model, scaler = load_lstm()
        scaled = scaler.transform([data])
        seq = scaled.reshape((1, 1, len(data)))
        prediction = float(model.predict(seq)[0][0])
    else:
        raise HTTPException(status_code=400, detail="Invalid model_type. Use: rf, xgb, lstm")

    return {
        "virus": payload.virus,
        "device_id": payload.device_id,
        "model_used": model_type,
        "predicted_time_to_detection": prediction,
    }

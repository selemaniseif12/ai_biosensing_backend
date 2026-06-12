from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.ml.classifier import classify

router = APIRouter()

class ClassifyRequest(BaseModel):
    features: List[float]

@router.post("/ml/classify")
def ml_classify(payload: ClassifyRequest):
    try:
        result = classify(payload.features)
        return {"class": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# app/routers/measurements.py

from fastapi import APIRouter, HTTPException
from app.database.session import SessionLocal, get_db

from app.schemas.measurement_schema import MeasurementCreate, MeasurementResponse
from app.services.measurement_service import (
    create_measurement,
    list_measurements,
    get_measurement,
    get_measurements_for_sample
)

router = APIRouter()

@router.post("/", response_model=MeasurementResponse)
def create_measurement_endpoint(data: MeasurementCreate):
    return create_measurement(data)

@router.get("/", response_model=list[MeasurementResponse])
def list_measurements_endpoint():
    return list_measurements()

@router.get("/{measurement_id}", response_model=MeasurementResponse)
def get_measurement_endpoint(measurement_id: str):
    measurement = get_measurement(measurement_id)
    if not measurement:
        raise HTTPException(status_code=404, detail="Measurement not found")
    return measurement

@router.get("/sample/{sample_id}", response_model=list[MeasurementResponse])
def get_measurements_for_sample_endpoint(sample_id: str):
    return get_measurements_for_sample(sample_id)

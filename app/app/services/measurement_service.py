# app/services/measurement_service.py

from uuid import uuid4
from app.models.measurement import Measurement

measurements_db = {}

def create_measurement(data):
    measurement_id = str(uuid4())
    measurement = Measurement(id=measurement_id, **data.dict())
    measurements_db[measurement_id] = measurement
    return measurement

def list_measurements():
    return list(measurements_db.values())

def get_measurement(measurement_id: str):
    return measurements_db.get(measurement_id)

def get_measurements_for_sample(sample_id: str):
    return [
        m for m in measurements_db.values()
        if m.sample_id == sample_id
    ]

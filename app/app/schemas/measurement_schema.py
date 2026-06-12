# app/schemas/measurement_schema.py

from pydantic import BaseModel
from datetime import datetime

class MeasurementBase(BaseModel):
    sample_id: str
    frequency_data: list[float]
    timestamp: datetime

class MeasurementCreate(MeasurementBase):
    pass

class MeasurementResponse(MeasurementBase):
    id: str

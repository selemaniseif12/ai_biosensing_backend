from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MeasurementBase(BaseModel):
    customer_id: int
    frequency: float
    amplitude: float
    phase: float


class MeasurementCreate(MeasurementBase):
    pass


class MeasurementUpdate(BaseModel):
    frequency: Optional[float] = None
    amplitude: Optional[float] = None
    phase: Optional[float] = None


class MeasurementOut(MeasurementBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

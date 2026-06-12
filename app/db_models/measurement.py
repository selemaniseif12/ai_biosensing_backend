from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from app.db_models.base import Base

class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, index=True)
    frequency = Column(Float, nullable=False)
    amplitude = Column(Float, nullable=False)
    phase = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

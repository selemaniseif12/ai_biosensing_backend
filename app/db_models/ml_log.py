# app/db_models/ml_log.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class MLLog(Base):
    __tablename__ = "ml_logs"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("ml_models.id"), nullable=False)
    run_id = Column(String, unique=True, nullable=False)
    status = Column(String, default="pending")
    duration = Column(Float)
    accuracy = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

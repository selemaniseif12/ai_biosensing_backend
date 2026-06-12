from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey
from app.database import Base

class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id", ondelete="CASCADE"))
    pathogen = Column(String(255))
    confidence = Column(Float)
    detected_at = Column(TIMESTAMP)

from sqlalchemy import Column, Integer, String, TIMESTAMP, JSON, ForeignKey
from app.database import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"))
    filename = Column(String(255))
    file_path = Column(String(500))
    meta = Column(JSON)  # renamed from metadata
    uploaded_at = Column(TIMESTAMP)

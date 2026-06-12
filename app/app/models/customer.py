from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db_models.base import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True)
    organization = Column(String(255))
    phone = Column(String(50))

    # Relationship to API keys
    api_keys = relationship("APIKey", back_populates="customer")

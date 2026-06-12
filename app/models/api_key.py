# app/models/api_key.py

import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from app.database import Base


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)

    # The actual API key string
    key = Column(String(128), unique=True, index=True, nullable=False)

    # Link to customer
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    # Optional name (e.g., "Production Key", "Test Key")
    name = Column(String(100), nullable=True)

    # Status
    active = Column(Boolean, default=True, nullable=False)
    revoked_at = Column(DateTime, nullable=True)

    # Usage tracking
    total_calls = Column(Integer, default=0, nullable=False)

    # Monthly usage limit (0 = unlimited)
    monthly_limit = Column(Integer, default=0, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship back to Customer
    customer = relationship("Customer", back_populates="api_keys")

    @staticmethod
    def generate_key() -> str:
        return uuid.uuid4().hex + uuid.uuid4().hex

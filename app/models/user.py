from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # REMOVE this line:
    # subscriptions = relationship("Subscription", back_populates="user")

    # REMOVE this line too (already done earlier):
    # cart_items = relationship("CartItem", back_populates="user")

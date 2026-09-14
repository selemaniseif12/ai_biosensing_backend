# app/models/products.py

from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    type = Column(String(50), nullable=False)
    price_usd = Column(Float, nullable=False)
    billing_period = Column(String(50), nullable=False)
    description = Column(String(500), nullable=True)

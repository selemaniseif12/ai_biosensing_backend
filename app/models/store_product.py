# app/models/store_product.py

from sqlalchemy import Column, Integer, String, Float
from app.database import Base  # <-- use the shared Base

class StoreProduct(Base):
    __tablename__ = "store_products"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    type = Column(String(50), nullable=False)  # physical, digital, course, service
    price_usd = Column(Float, nullable=False)
    billing_period = Column(String(50), nullable=False)  # one_time or 3_months
    description = Column(String(500), nullable=True)

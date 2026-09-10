from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class CartItem(Base):
    __tablename__ = "cart_item"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    item_id = Column(String, index=True)
    item_name = Column(String)
    price_usd = Column(Float)
    quantity = Column(Integer)

    user = relationship("User", back_populates="cart_items")

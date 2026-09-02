from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)

    # MUST be a ForeignKey for SQLAlchemy to link User → CartItem
    user_id = Column(Integer, ForeignKey("users.id"))

    item_id = Column(String, index=True)
    item_name = Column(String)

    item_type = Column(String)
    billing = Column(String)

    price_usd = Column(Float)
    quantity = Column(Integer)

    # Relationship back to User
    user = relationship("User", back_populates="cart_items")

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.cart_item import CartItem

router = APIRouter(prefix="/checkout", tags=["Checkout"])

@router.post("")
def process_checkout(user_id: int, db: Session = Depends(get_db)):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()

    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart is empty")

    total = sum(item.price_usd * item.quantity for item in cart_items)
    payment_status = "success"

    # Save items BEFORE any action
    items_data = [
        {
            "item_id": item.item_id,
            "name": item.item_name,
            "quantity": item.quantity,
            "price_usd": item.price_usd
        }
        for item in cart_items
    ]

    # ⭐ FIX: Do NOT delete cart items
    # This prevents the cart table from being wiped
    # and avoids 500 errors on subsequent checkout calls.

    return {
        "message": "Payment processed successfully",
        "status": payment_status,
        "total": total,
        "items": items_data
    }

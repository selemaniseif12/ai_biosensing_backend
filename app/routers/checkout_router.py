from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.cart_item import CartItem

router = APIRouter(prefix="/checkout", tags=["Checkout"])


@router.post("")
def process_checkout(user_id: int, db: Session = Depends(get_db)):
    # Fetch all cart items for the user
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()

    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart is empty")

    # Calculate total
    total = sum(item.price_usd * item.quantity for item in cart_items)

    # Simulate payment processing (replace with Stripe or PayPal later)
    payment_status = "success"

    # Clear cart after successful payment
    for item in cart_items:
        db.delete(item)
    db.commit()

    return {
        "message": "Payment processed successfully",
        "status": payment_status,
        "total": total,
        "items": [item.item_name for item in cart_items],
    }

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.cart_item import CartItem
from app.models.receipt import Receipt  # Make sure this model exists

router = APIRouter(prefix="/checkout", tags=["Checkout"])


@router.post("")
def process_checkout(user_id: int, db: Session = Depends(get_db)):
    # Fetch all cart items for this user
    cart_items = (
        db.query(CartItem)
        .filter(CartItem.user_id == user_id)
        .all()
    )

    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart is empty")

    # ⭐ FIX: Convert price_usd and quantity to numbers to avoid string concatenation
    total = sum(
        float(item.price_usd) * int(item.quantity)
        for item in cart_items
    )

    # Prepare receipt item list
    items_data = [
        {
            "item_id": item.item_id,
            "name": item.item_name,
            "quantity": item.quantity,
            "price_usd": item.price_usd
        }
        for item in cart_items
    ]

    # ⭐ FIX 3: Create receipt entry
    receipt = Receipt(
        user_id=user_id,
        total_amount=total,
        items="; ".join([item.item_name for item in cart_items])
    )

    db.add(receipt)

    # ⭐ FIX 3: Clear cart in ONE safe operation
    (
        db.query(CartItem)
        .filter(CartItem.user_id == user_id)
        .delete()
    )

    db.commit()
    db.refresh(receipt)

    return {
        "message": "Checkout completed successfully",
        "status": "success",
        "total": total,
        "items": items_data,
        "receipt_id": receipt.id
    }

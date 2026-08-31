import stripe
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.cart_item import CartItem
from app.models.receipt import Receipt
import json
from datetime import datetime

router = APIRouter(tags=["Stripe"])

import os
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


# ---------------------------------------------------------
# Create Stripe Checkout Session
# ---------------------------------------------------------
@router.post("/stripe/checkout")
def stripe_checkout(user_id: int, db: Session = Depends(get_db)):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    line_items = []
    for item in cart_items:
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": item.item_name
                },
                "unit_amount": int(item.price_usd * 100)
            },
            "quantity": item.quantity
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url="http://localhost/dashboard/admin/checkout?success=true",
        cancel_url="http://localhost/dashboard/admin/checkout?canceled=true",
        metadata={"user_id": user_id}
    )

    return {"checkout_url": session.url}

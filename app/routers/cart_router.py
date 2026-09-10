from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.cart_item import CartItem

router = APIRouter(prefix="/store/cart", tags=["Cart"])

# JSON model for cart requests
class CartAddRequest(BaseModel):
    item_id: str   # <-- FIXED: item_id is STRING


@router.get("")
def get_cart(user_id: int, db: Session = Depends(get_db)):
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()


@router.post("/add")
def add_to_cart(user_id: int, payload: CartAddRequest, db: Session = Depends(get_db)):
    # Fetch product directly from DB using string item_id
    product = db.query(CartItem).filter(CartItem.item_id == payload.item_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Store item not found")

    # Create a new cart entry
    cart_item = CartItem(
        user_id=user_id,
        item_id=product.item_id,
        item_name=product.item_name,
        quantity=1,
        price_usd=product.price_usd
    )

    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return {
        "message": "Added to cart",
        "item": {
            "item_id": cart_item.item_id,
            "item_name": cart_item.item_name,
            "quantity": cart_item.quantity,
            "price_usd": cart_item.price_usd
        }
    }


@router.delete("/delete")
def delete_cart_item(user_id: int, item_id: str, db: Session = Depends(get_db)):
    item = db.query(CCartItem).filter(
        CartItem.user_id == user_id,
        CartItem.item_id == item_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()

    return {"message": "Item deleted"}


# -----------------------------------------------------------
# Alias routes
# -----------------------------------------------------------

alias_router = APIRouter(tags=["Cart Alias"])

@alias_router.post("/cart/add")
def alias_add_to_cart(user_id: int, payload: CartAddRequest, db: Session = Depends(get_db)):
    return add_to_cart(user_id=user_id, payload=payload, db=db)

@alias_router.get("/cart")
def alias_get_cart(user_id: int, db: Session = Depends(get_db)):
    return get_cart(user_id=user_id, db=db)

@alias_router.delete("/cart/delete")
def alias_delete_cart_item(user_id: int, item_id: str, db: Session = Depends(get_db)):
    return delete_cart_item(user_id=user_id, item_id=item_id, db=db)

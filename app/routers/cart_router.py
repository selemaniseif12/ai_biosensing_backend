from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.cart_item import CartItem
from app.routers.store_router import get_products

router = APIRouter(prefix="/store/cart", tags=["Cart"])

# JSON model for cart requests
class CartAddRequest(BaseModel):
    item_id: int
    user_id: int


@router.get("")
def get_cart(user_id: int, db: Session = Depends(get_db)):
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()


@router.post("/add")
def add_to_cart(payload: CartAddRequest, db: Session = Depends(get_db)):
    store_items = get_products()
    store_item = next((item for item in store_items if item["id"] == payload.item_id), None)

    if not store_item:
        raise HTTPException(status_code=404, detail="Store item not found")

    cart_item = CartItem(
        item_id=payload.item_id,
        user_id=payload.user_id,
        item_name=store_item["name"],
        item_type=store_item["type"],
        billing=store_item["billing"],
        price_usd=store_item["price"],
        quantity=1
    )

    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return {"message": "Added to cart", "item": cart_item}


@router.delete("/delete")
def delete_cart_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(CartItem).filter(CartItem.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()

    return {"message": "Item deleted"}


# -----------------------------------------------------------
# Alias routes for government homepage
# -----------------------------------------------------------

alias_router = APIRouter(tags=["Cart Alias"])

@alias_router.post("/cart/add")
def alias_add_to_cart(payload: CartAddRequest, db: Session = Depends(get_db)):
    return add_to_cart(payload=payload, db=db)

@alias_router.get("/cart")
def alias_get_cart(user_id: int, db: Session = Depends(get_db)):
    return get_cart(user_id=user_id, db=db)

@alias_router.delete("/cart/delete")
def alias_delete_cart_item(item_id: int, db: Session = Depends(get_db)):
    return delete_cart_item(item_id=item_id, db=db)

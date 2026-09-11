from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.products import Product

router = APIRouter(prefix="/store", tags=["Store"])


@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    """
    Return all products from the real database table `products`.
    """
    products = db.query(Product).all()
    return products


@router.get("/product/{item_id}")
def get_product(item_id: str, db: Session = Depends(get_db)):
    """
    Return a single product by its item_id.
    """
    product = db.query(Product).filter(Product.item_id == item_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Item not found")
    return product

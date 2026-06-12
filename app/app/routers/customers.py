from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal, get_db

from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerOut
from app.crud import customers as crud_customers

router = APIRouter(tags=["Customers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[CustomerOut])
def list_customers(db: Session = Depends(get_db)):
    return crud_customers.get_customers(db)

@router.post("/", response_model=CustomerOut)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return crud_customers.create_customer(db, customer)

@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    return crud_customers.get_customer(db, customer_id)

@router.put("/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    return crud_customers.update_customer(db, customer_id, customer)

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    return crud_customers.delete_customer(db, customer_id)

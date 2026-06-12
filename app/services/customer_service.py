# app/services/customer_service.py

from uuid import uuid4
from app.models.customer import Customer
from app.schemas.customer_schema import CustomerCreate, CustomerResponse

# In‑memory storage
customers_db = {}

def create_customer(data: CustomerCreate) -> CustomerResponse:
    customer_id = str(uuid4())
    customer = Customer(id=customer_id, **data.dict())
    customers_db[customer_id] = customer
    return CustomerResponse(**customer.dict())

def list_customers() -> list[CustomerResponse]:
    return [CustomerResponse(**c.dict()) for c in customers_db.values()]

def get_customer(customer_id: str) -> Customer | None:
    return customers_db.get(customer_id)

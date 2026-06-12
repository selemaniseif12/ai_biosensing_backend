from pydantic import BaseModel

class CustomerBase(BaseModel):
    name: str
    email: str | None = None
    organization: str | None = None
    phone: str | None = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class CustomerOut(CustomerBase):
    id: int

    class Config:
        orm_mode = True

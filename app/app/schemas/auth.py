from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserOut(UserBase):
    id: int
    is_active: bool
    role: str

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: str
    password: str
    role: str = "user"

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
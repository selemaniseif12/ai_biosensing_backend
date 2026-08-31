from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.dependencies import get_db
from app.schemas.auth import UserCreate
from app.services.auth_service import register_user
from app.models.user import User
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth")

SECRET_KEY = "564cc7b73913e7206a15fd72385738d779e04957686233143ffe68b22c77b5c7"
ALGORITHM = "HS256"

# ---------------------------------------------------------
# REGISTER
# ---------------------------------------------------------
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db)

# ---------------------------------------------------------
# LOGIN (JSON email + password)
# ---------------------------------------------------------
class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == data.email).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(data.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": db_user.id})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": db_user.id,
        "email": db_user.email
    }

# ---------------------------------------------------------
# ADMIN — LIST USERS
# ---------------------------------------------------------
@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import UserCreate, UserLogin
from app.services.auth_service import register_user, authenticate_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(user.email, user.password, db)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "access_token": "dummy",  # your token logic is inside auth_service
        "email": db_user.email,
        "user_id": db_user.id
    }

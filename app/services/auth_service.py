from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import UserCreate
from app.utils.hashing import hash_password, verify_password

def register_user(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    new_user = User(email=user.email, password=hashed_pw)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user

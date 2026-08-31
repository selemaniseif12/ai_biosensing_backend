from sqlalchemy.orm import Session
from fastapi import HTTPException

# ✅ Use the SUBSCRIPTION User model
from app.models.user import User

from app.schemas.auth import UserCreate, UserLogin
from app.core.security import verify_password, get_password_hash, create_access_token


def register_user(user: UserCreate, db: Session):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)

    new_user = User(
        email=user.email,
        password_hash=hashed_password   # subscription model uses password_hash
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


def login_user(user: UserLogin, db: Session):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # ⭐ FIXED: use user.id instead of email
    token = create_access_token({"sub": db_user.id})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": db_user.id,
        "email": db_user.email
    }

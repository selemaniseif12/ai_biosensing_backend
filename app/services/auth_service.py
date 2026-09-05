from sqlalchemy.orm import Session
from fastapi import HTTPException

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
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


# ⭐ Added authenticate_user (this fixes your ImportError)
def authenticate_user(email: str, password: str, db: Session):
    db_user = db.query(User).filter(User.email == email).first()

    if not db_user:
        return None

    if not verify_password(password, db_user.password_hash):
        return None

    return db_user


def login_user(user: UserLogin, db: Session):
    db_user = authenticate_user(user.email, user.password, db)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": db_user.id})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": db_user.id,
        "email": db_user.email
    }

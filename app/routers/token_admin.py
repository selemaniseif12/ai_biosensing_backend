from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.token_model import ServiceToken

router = APIRouter(prefix="/services", tags=["Subscribed Services"])

# ---------------------------------------------------------
# EXISTING ROUTES (UNCHANGED)
# ---------------------------------------------------------

@router.get("/consulting")
async def consulting_service(db: Session = Depends(get_db)):
    return {"access": "consulting_granted"}

@router.get("/course/{course_id}")
async def course_service(course_id: str, db: Session = Depends(get_db)):
    return {"access": f"course_{course_id}_granted"}

@router.get("/ml/{model_id}")
async def ml_model_service(model_id: str, db: Session = Depends(get_db)):
    return {"access": f"ml_model_{model_id}_granted"}

@router.get("/virus-list")
async def virus_list_service(db: Session = Depends(get_db)):
    return {"access": "virus_list_granted"}


# ---------------------------------------------------------
# ⭐ NEW ADMIN TOKEN MANAGEMENT SECTION
# ---------------------------------------------------------

admin_router = APIRouter(prefix="/admin/tokens", tags=["Admin Token Control"])


@admin_router.get("/list")
def list_tokens(db: Session = Depends(get_db)):
    """List all tokens."""
    tokens = db.query(ServiceToken).all()
    return tokens


@admin_router.post("/create")
def create_token(service_name: str, user_id: int | None = None, db: Session = Depends(get_db)):
    """Manually create a new token."""
    token_obj = ServiceToken.create_token(
        db=db,
        service_name=service_name,
        user_id=user_id
    )
    return {
        "status": "created",
        "token": token_obj.token,
        "service": service_name,
        "user_id": user_id
    }


@admin_router.post("/disable/{token}")
def disable_token(token: str, db: Session = Depends(get_db)):
    """Disable an existing token."""
    token_obj = db.query(ServiceToken).filter(ServiceToken.token == token).first()

    if not token_obj:
        raise HTTPException(status_code=404, detail="Token not found")

    token_obj.is_active = False
    db.commit()

    return {"status": "disabled", "token": token}


@admin_router.post("/activate/{token}")
def activate_token(token: str, db: Session = Depends(get_db)):
    """Re-activate a disabled token."""
    token_obj = db.query(ServiceToken).filter(ServiceToken.token == token).first()

    if not token_obj:
        raise HTTPException(status_code=404, detail="Token not found")

    token_obj.is_active = True
    db.commit()

    return {"status": "activated", "token": token}


@admin_router.post("/extend/{token}")
def extend_token_expiration(token: str, days: int = 30, db: Session = Depends(get_db)):
    """Extend token expiration."""
    token_obj = db.query(ServiceToken).filter(ServiceToken.token == token).first()

    if not token_obj:
        raise HTTPException(status_code=404, detail="Token not found")

    from datetime import datetime, timedelta
    token_obj.expires_at = datetime.utcnow() + timedelta(days=days)
    db.commit()

    return {
        "status": "extended",
        "token": token,
        "new_expiration": token_obj.expires_at
    }


# ---------------------------------------------------------
# ⭐ REGISTER ADMIN ROUTER
# ---------------------------------------------------------

router.include_router(admin_router)

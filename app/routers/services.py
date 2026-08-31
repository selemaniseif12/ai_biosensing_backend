# routers/services.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.token_model import ServiceToken
from pydantic import BaseModel

router = APIRouter(prefix="/services", tags=["Subscribed Services"])


# ---------------------------------------------------------
# Shared token validator (UPDATED)
# ---------------------------------------------------------
def validate_token(db: Session, token: str, service_name: str):
    # Normalize service_name so numeric IDs like "1" become "course_1"
    normalized = f"course_{service_name}"

    record = (
        db.query(ServiceToken)
        .filter(
            ServiceToken.token == token,
            ServiceToken.service_name == normalized,
            ServiceToken.is_active == True
        )
        .first()
    )

    if not record:
        raise HTTPException(status_code=403, detail="Invalid or inactive token")

    return True


# ---------------------------------------------------------
# Consulting Access
# ---------------------------------------------------------
@router.get("/consulting")
async def consulting_service(token: str, db: Session = Depends(get_db)):
    validate_token(db, token, "consulting_fixed")
    return {"access": "consulting_granted"}


# ---------------------------------------------------------
# Course Access
# ---------------------------------------------------------
@router.get("/course/{course_id}")
async def course_service(course_id: str, token: str, db: Session = Depends(get_db)):
    validate_token(db, token, course_id)
    return {"access": f"course_{course_id}_granted"}


# ---------------------------------------------------------
# ML Model Access
# ---------------------------------------------------------
@router.get("/ml/{model_id}")
async def ml_model_service(model_id: str, token: str, db: Session = Depends(get_db)):
    validate_token(db, token, model_id)
    return {"access": f"ml_model_{model_id}_granted"}


# ---------------------------------------------------------
# Virus Database Access
# ---------------------------------------------------------
@router.get("/virus-list")
async def virus_list_service(token: str, db: Session = Depends(get_db)):
    validate_token(db, token, "virus_list")
    return {"access": "virus_list_granted"}

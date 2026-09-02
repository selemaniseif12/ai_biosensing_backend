from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.service_token_model import ServiceToken



# ---------------------------------------------------------
# CREATE TOKEN (LEGACY RESTORED)
# ---------------------------------------------------------
def create_token(db: Session, service_name: str, user_id: int | None = None):
    """
    Legacy token creation restored.
    Accepts:
    {
      "service_name": "v6",
      "user_id": 1974
    }
    """

    import secrets
    token_value = secrets.token_hex(16)

    token_record = ServiceToken(
        token=token_value,
        token_type=service_name,      # REQUIRED for v2/v6/VirusList
        service_name=service_name,
        user_id=user_id,
        is_active=True,
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(days=30)
    )

    db.add(token_record)
    db.commit()
    db.refresh(token_record)

    return token_record


# ---------------------------------------------------------
# CHECK IF TOKEN IS ACTIVE (LEGACY)
# ---------------------------------------------------------
def is_token_active(db: Session, token: str, service_name: str) -> bool:
    """
    Checks if a token is active and matches the service.
    Used by routers before loading dashboards or APIs.
    """
    record = (
        db.query(ServiceToken)
        .filter(
            ServiceToken.token == token,
            ServiceToken.token_type == service_name,
            ServiceToken.is_active == True
        )
        .first()
    )
    return record is not None


# ---------------------------------------------------------
# DEACTIVATE TOKEN (LEGACY)
# ---------------------------------------------------------
def deactivate_token(db: Session, token: str) -> bool:
    """
    Deactivates a token (admin or system).
    """
    record = (
        db.query(ServiceToken)
        .filter(ServiceToken.token == token)
        .first()
    )

    if not record:
        return False

    record.is_active = False
    db.commit()
    return True

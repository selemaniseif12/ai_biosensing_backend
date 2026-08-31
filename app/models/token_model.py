from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database import Base

class ServiceToken(Base):
    __tablename__ = "service_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)

    # ⭐ RESTORED FIELD — REQUIRED FOR V2/V6/VirusList
    token_type = Column(String, nullable=False)

    # ⭐ REQUIRED BY YOUR ORIGINAL ROUTER
    service_name = Column(String, nullable=False)

    user_id = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

    @staticmethod
    def create_token(db, service_name, user_id=None):
        import secrets
        token_value = secrets.token_hex(16)

        token = ServiceToken(
            token=token_value,
            token_type=service_name,      # ⭐ MUST MATCH VALIDATION
            service_name=service_name,
            user_id=user_id,
            is_active=True
        )

        db.add(token)
        db.commit()
        db.refresh(token)
        return token

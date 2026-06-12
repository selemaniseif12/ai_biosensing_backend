from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from app.database import SessionLocal


class AnalyticsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Create DB session
        db: Session = SessionLocal()

        try:
            # Process request
            response = await call_next(request)

            # No logging because UsageLog model was removed
            return response

        finally:
            db.close()

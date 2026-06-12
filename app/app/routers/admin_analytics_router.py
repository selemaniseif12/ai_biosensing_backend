from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import String

from app.database.session import get_db
from app.database.models import AnalysisLog

router = APIRouter(
    prefix="/analytics",
    tags=["Admin Analytics"]
)

@router.get("/logs")
def get_all_logs(db: Session = Depends(get_db)):
    """
    Return all analysis logs for admin analytics dashboard.
    """
    logs = (
        db.query(AnalysisLog)
        .order_by(AnalysisLog.created_at.desc())
        .all()
    )
    return logs


@router.get("/logs/version/{version}")
def get_logs_by_version(version: str, db: Session = Depends(get_db)):
    """
    Filter logs by analyzer version (e.g., v6).
    """
    logs = (
        db.query(AnalysisLog)
        .filter(AnalysisLog.version == version)
        .order_by(AnalysisLog.created_at.desc())
        .all()
    )
    return logs


@router.get("/logs/date/{date}")
def get_logs_by_date(date: str, db: Session = Depends(get_db)):
    """
    Filter logs by date (YYYY-MM-DD).
    """
    try:
        logs = (
            db.query(AnalysisLog)
            .filter(AnalysisLog.created_at.cast(String).like(f"{date}%"))
            .order_by(AnalysisLog.created_at.desc())
            .all()
        )
        return logs
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use YYYY-MM-DD."
        )

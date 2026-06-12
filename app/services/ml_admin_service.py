from sqlalchemy.orm import Session
from app.db_models.ml_log import MLLog


# ---------------------------------------------------------
# List all ML logs
# ---------------------------------------------------------
def service_list_ml_logs(db: Session):
    return db.query(MLLog).all()

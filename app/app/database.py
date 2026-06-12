from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------------------------------------------------
# SQLAlchemy Base
# ---------------------------------------------------------
Base = declarative_base()

# ---------------------------------------------------------
# Database URL (SQLite)
# NOTE:
# - This creates a permanent SQLite file named app.db
# - Located in the project root
# - Works with all existing models
# ---------------------------------------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ---------------------------------------------------------
# FastAPI Dependency
# ---------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------
# Import all models so SQLAlchemy registers them
# ---------------------------------------------------------
import app.models.user
import app.models.customer
import app.models.measurement
import app.models.dataset
import app.models.detection
import app.models.ml_log
import app.models.usage_log
import app.models.api_key

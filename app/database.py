# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------------------------------------------------
# PostgreSQL connection (your existing configuration)
# ---------------------------------------------------------
DATABASE_URL = "postgresql://postgres:Magazijuto74@localhost:5432/ai_biosensing"

# ---------------------------------------------------------
# SQLAlchemy Engine
# ---------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# ---------------------------------------------------------
# Session Factory
# ---------------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ---------------------------------------------------------
# Shared Base used by ALL models
# ---------------------------------------------------------
Base = declarative_base()

# ---------------------------------------------------------
# Dependency for FastAPI routes
# ---------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------
# IMPORTANT: Create all tables on startup
# ---------------------------------------------------------
def init_db():
    """
    Ensures all SQLAlchemy models create their tables in PostgreSQL.
    This includes your existing models AND the new receipt model.
    """

    # Existing models
    from app.models.consulting_model import ConsultingRequestModel
    from app.models.token_model import ServiceToken
    from app.models.service_model import Service

    # NEW: Receipt model
    from app.models.receipt import Receipt

    # Create all tables
    Base.metadata.create_all(bind=engine)

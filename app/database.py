import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Add it in your .env file.")

# ---------------------------------------------------------
# SQLAlchemy Engine (Neon PostgreSQL)
# ---------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
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
# Base Model
# ---------------------------------------------------------
Base = declarative_base()

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
# Create all tables in Neon
# ---------------------------------------------------------
def init_db():
    """
    Ensures all SQLAlchemy models create their tables in Neon PostgreSQL.
    """

    # Import ALL models so SQLAlchemy knows them
    from app.models.token_model import TokenModel
    from app.models.consulting_model import ConsultingRequestModel
    from app.models.service_model import Service
    from app.models.receipt import Receipt
    from app.models.cart_item import CartItem   # ⭐ REQUIRED

    Base.metadata.create_all(bind=engine)

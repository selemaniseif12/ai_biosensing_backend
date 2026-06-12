from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./app.db"  # or your PostgreSQL URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # remove this if using PostgreSQL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

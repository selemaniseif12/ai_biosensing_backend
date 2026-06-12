from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal, get_db

from app.schemas.sample import SampleCreate, SampleOut
from app.crud import samples as crud_samples

router = APIRouter(tags=["Samples"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[SampleOut])
def list_samples(db: Session = Depends(get_db)):
    return crud_samples.get_samples(db)

@router.post("/", response_model=SampleOut)
def create_sample(sample: SampleCreate, db: Session = Depends(get_db)):
    return crud_samples.create_sample(db, sample)

@router.get("/{sample_id}", response_model=SampleOut)
def get_sample(sample_id: int, db: Session = Depends(get_db)):
    return crud_samples.get_sample(db, sample_id)

from sqlalchemy.orm import Session
from app.db_models.sample import Sample
from app.schemas.sample import SampleCreate

def get_samples(db: Session):
    return db.query(Sample).all()

def get_sample(db: Session, sample_id: int):
    return db.query(Sample).filter(Sample.id == sample_id).first()

def create_sample(db: Session, sample: SampleCreate):
    db_sample = Sample(
        name=sample.name,
        description=sample.description
    )
    db.add(db_sample)
    db.commit()
    db.refresh(db_sample)
    return db_sample

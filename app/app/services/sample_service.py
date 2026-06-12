from app.models.sample import Sample
from app.schemas.sample_schema import SampleCreate, SampleResponse
from typing import List
from uuid import uuid4

# Temporary in-memory storage
samples_db: List[Sample] = []


def create_sample(data: SampleCreate) -> SampleResponse:
    sample = Sample(
        id=str(uuid4()),
        customer_id=data.customer_id,
        sample_type=data.sample_type,
        description=data.description,
        created_at=data.created_at
    )
    samples_db.append(sample)
    return SampleResponse(**sample.dict())


def list_samples() -> List[SampleResponse]:
    return [SampleResponse(**s.dict()) for s in samples_db]


def get_sample(sample_id: str) -> SampleResponse | None:
    for s in samples_db:
        if s.id == sample_id:
            return SampleResponse(**s.dict())
    return None

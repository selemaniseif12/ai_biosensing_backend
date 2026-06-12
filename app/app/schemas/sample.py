from pydantic import BaseModel

class SampleBase(BaseModel):
    name: str
    description: str | None = None

class SampleCreate(SampleBase):
    pass

class SampleOut(SampleBase):
    id: int

    class Config:
        orm_mode = True

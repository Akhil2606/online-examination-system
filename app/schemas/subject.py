from pydantic import BaseModel


class SubjectCreate(BaseModel):
    subject_name: str


class SubjectResponse(BaseModel):
    id: int
    subject_name: str

    class Config:
        from_attributes = True
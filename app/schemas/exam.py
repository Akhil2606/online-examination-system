from pydantic import BaseModel


class ExamCreate(BaseModel):

    exam_name: str

    subject_id: int

    duration: int

    passing_marks: int


class ExamQuestionCreate(BaseModel):

    exam_id: int

    question_id: int
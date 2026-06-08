from pydantic import BaseModel


class StartExam(BaseModel):

    exam_id: int

from typing import List


class Answer(BaseModel):

    question_id: int
    selected_answer: str


class SubmitExam(BaseModel):

    exam_id: int

    answers: List[Answer]
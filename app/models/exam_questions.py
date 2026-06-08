from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from app.core.database import Base


class ExamQuestion(Base):

    __tablename__ = "exam_questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    exam_id = Column(
        Integer,
        ForeignKey("exams.id")
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id")
    )
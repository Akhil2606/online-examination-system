from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from app.core.database import Base


class Exam(Base):

    __tablename__ = "exams"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    exam_name = Column(
        String(100),
        nullable=False
    )

    subject_id = Column(
        Integer,
        ForeignKey("subjects.id")
    )

    duration = Column(
        Integer,
        nullable=False
    )

    passing_marks = Column(
        Integer,
        nullable=False
    )
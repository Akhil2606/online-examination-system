from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from app.core.database import Base

from sqlalchemy import DateTime

from datetime import datetime


class StudentExam(Base):

    __tablename__ = "student_exams"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    exam_id = Column(
        Integer,
        ForeignKey("exams.id")
    )

    score = Column(
        Integer,
        default=0
    )

    start_time = Column(
    DateTime,
    default=datetime.utcnow
)
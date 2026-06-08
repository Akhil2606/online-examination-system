from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from app.core.database import Base


class Result(Base):

    __tablename__ = "results"

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

    total_score = Column(
        Integer
    )

    status = Column(
        String(20)
    )
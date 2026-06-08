from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from app.core.database import Base


class Question(Base):

    __tablename__ = "questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    subject_id = Column(
        Integer,
        ForeignKey("subjects.id")
    )

    question_text = Column(
        String(500),
        nullable=False
    )

    option_a = Column(
        String(200),
        nullable=False
    )

    option_b = Column(
        String(200),
        nullable=False
    )

    option_c = Column(
        String(200),
        nullable=False
    )

    option_d = Column(
        String(200),
        nullable=False
    )

    correct_answer = Column(
        String(1),
        nullable=False
    )
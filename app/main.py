from fastapi import FastAPI

from app.core.database import engine
from app.core.database import Base

from app.models.role import Role
from app.models.user import User
from app.models.subject import Subject
from app.models.question import Question
from app.models.exam import Exam
from app.models.exam_questions import ExamQuestion
from app.schemas.subject import SubjectCreate
from app.models.student_exam import StudentExam
from app.models.result import Result

from app.routers.auth import router as auth_router
from app.routers.subjects import router as subject_router
from app.routers.questions import router as question_router
from app.routers.exams import router as exam_router
from app.routers.student_exam import router as student_exam_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Online Examination System"
)

app.include_router(auth_router)
app.include_router(subject_router)
app.include_router(question_router)
app.include_router(exam_router)
app.include_router(student_exam_router)

@app.get("/")
def home():
    return {
        "message": "Online Examination System API Running"
    }
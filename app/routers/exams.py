from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
import openpyxl

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.exam import Exam
from app.models.subject import Subject
from app.schemas.exam import ExamCreate
from app.models.question import Question
from app.models.result import Result
from app.models.user import User
from app.models.exam_questions import ExamQuestion
from app.schemas.exam import ExamQuestionCreate
from fastapi.responses import FileResponse
from app.core.permissions import admin_required

router = APIRouter(
    prefix="/exams",
    tags=["Exams"]
)

@router.post("/")
def create_exam(
    exam: ExamCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    subject = db.query(Subject).filter(
        Subject.id == exam.subject_id
    ).first()

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    new_exam = Exam(
        exam_name=exam.exam_name,
        subject_id=exam.subject_id,
        duration=exam.duration,
        passing_marks=exam.passing_marks
    )

    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)

    return {
        "message": "Exam created successfully"
    }

@router.get("/")
def get_all_exams(
    db: Session = Depends(get_db)
):

    exams = db.query(Exam).all()

    return exams

@router.post("/assign-question")
def assign_question(
    data: ExamQuestionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    exam = db.query(Exam).filter(
        Exam.id == data.exam_id
    ).first()

    if not exam:
        raise HTTPException(
            status_code=404,
            detail="Exam not found"
        )

    question = db.query(Question).filter(
        Question.id == data.question_id
    ).first()

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    exam_question = ExamQuestion(
        exam_id=data.exam_id,
        question_id=data.question_id
    )

    db.add(exam_question)
    db.commit()

    return {
        "message": "Question assigned successfully"
    }

@router.get("/top-scorers")
def top_scorers(
    db: Session = Depends(get_db)
):

    results = db.query(Result).order_by(
        Result.total_score.desc()
    ).all()

    return results

@router.get("/statistics")
def exam_statistics(
    db: Session = Depends(get_db)
):

    total_exams = db.query(Exam).count()

    total_results = db.query(Result).count()

    return {
        "total_exams": total_exams,
        "total_results": total_results
    }

@router.get("/leaderboard")
def leaderboard(
    db: Session = Depends(get_db)
):

    results = db.query(Result).order_by(
        Result.total_score.desc()
    ).all()

    leaderboard_data = []

    for result in results:

        user = db.query(User).filter(
            User.id == result.student_id
        ).first()

        leaderboard_data.append(
            {
                "student_name": user.name,
                "exam_id": result.exam_id,
                "score": result.total_score,
                "status": result.status
            }
        )

    return leaderboard_data

@router.get("/export-results")
def export_results(
    db: Session = Depends(get_db)
):

    workbook = openpyxl.Workbook()

    sheet = workbook.active

    sheet.append(
        [
            "Student ID",
            "Exam ID",
            "Score",
            "Status"
        ]
    )

    results = db.query(Result).all()

    for result in results:

        sheet.append(
            [
                result.student_id,
                result.exam_id,
                result.total_score,
                result.status
            ]
        )

    file_name = "results.xlsx"

    workbook.save(file_name)

    return FileResponse(
        path=file_name,
        filename=file_name
    )
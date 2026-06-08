from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from datetime import datetime
from datetime import timedelta
from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.exam import Exam
from app.models.exam_questions import ExamQuestion
from app.models.question import Question
from app.models.student_exam import StudentExam
from app.schemas.student_exam import SubmitExam
from app.models.result import Result

from app.schemas.student_exam import StartExam

router = APIRouter(
    prefix="/student-exam",
    tags=["Student Exam"]
)

@router.post("/start")
def start_exam(
    data: StartExam,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    exam = db.query(Exam).filter(
        Exam.id == data.exam_id
    ).first()

    if not exam:
        raise HTTPException(
            status_code=404,
            detail="Exam not found"
        )

    student_exam = StudentExam(
        student_id=current_user["user_id"],  # temporary
        exam_id=data.exam_id
    )

    db.add(student_exam)
    db.commit()

    exam_questions = db.query(
        ExamQuestion
    ).filter(
        ExamQuestion.exam_id == data.exam_id
    ).all()

    question_list = []

    for item in exam_questions:

        question = db.query(
            Question
        ).filter(
            Question.id == item.question_id
        ).first()

        if question:

            question_list.append(
                {
                    "id": question.id,
                    "question_text": question.question_text,
                    "option_a": question.option_a,
                    "option_b": question.option_b,
                    "option_c": question.option_c,
                    "option_d": question.option_d
                }
            )

    return {
        "exam_name": exam.exam_name,
        "duration": exam.duration,
        "questions": question_list
    }

@router.post("/submit")
def submit_exam(
    data: SubmitExam,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    exam = db.query(Exam).filter(
        Exam.id == data.exam_id
    ).first()

    if not exam:
        raise HTTPException(
            status_code=404,
            detail="Exam not found"
        )

    # Check if student already submitted
    existing_result = db.query(Result).filter(
        Result.student_id == current_user["user_id"],
        Result.exam_id == data.exam_id
    ).first()

    if existing_result:
        raise HTTPException(
            status_code=400,
            detail="You have already submitted this exam"
        )

    # Get latest started exam
    student_exam = db.query(StudentExam).filter(
        StudentExam.student_id == current_user["user_id"],
        StudentExam.exam_id == data.exam_id
    ).order_by(
        StudentExam.id.desc()
    ).first()

    if not student_exam:
        raise HTTPException(
            status_code=400,
            detail="Exam not started"
        )

    # Timer validation
    allowed_time = student_exam.start_time + timedelta(
        minutes=exam.duration
    )

    if datetime.utcnow() > allowed_time:
        raise HTTPException(
            status_code=400,
            detail="Exam Time Expired"
        )

    # Calculate score
    score = 0

    for answer in data.answers:

        question = db.query(Question).filter(
            Question.id == answer.question_id
        ).first()

        if question:

            if (
                question.correct_answer.strip().upper()
                ==
                answer.selected_answer.strip().upper()
            ):
                score += 1

    # Pass / Fail
    status = "FAIL"

    if score >= exam.passing_marks:
        status = "PASS"

    # Update student_exam score
    student_exam.score = score

    # Save result
    result = Result(
        student_id=current_user["user_id"],
        exam_id=data.exam_id,
        total_score=score,
        status=status
    )

    db.add(result)
    db.commit()

    return {
        "exam_id": data.exam_id,
        "score": score,
        "passing_marks": exam.passing_marks,
        "status": status
    }

@router.get("/results")
def view_results(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    results = db.query(Result).filter(
        Result.student_id == current_user["user_id"]
    ).all()

    return results

@router.get("/history")
def exam_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    exams = db.query(StudentExam).filter(
        StudentExam.student_id == current_user["user_id"]
    ).all()

    return exams
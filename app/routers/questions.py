from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
import random

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.question import Question
from app.models.subject import Subject
from app.schemas.question import QuestionCreate
from app.core.permissions import admin_required

router = APIRouter(
    prefix="/questions",
    tags=["Questions"]
)

@router.post("/")
def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    subject = db.query(Subject).filter(
        Subject.id == question.subject_id
    ).first()

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    new_question = Question(
        subject_id=question.subject_id,
        question_text=question.question_text,
        option_a=question.option_a,
        option_b=question.option_b,
        option_c=question.option_c,
        option_d=question.option_d,
        correct_answer=question.correct_answer
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return {
        "message": "Question added successfully"
    }

@router.get("/")
def get_all_questions(
    db: Session = Depends(get_db)
):

    questions = db.query(Question).all()

    return questions

@router.get("/{question_id}")
def get_question_by_id(
    question_id: int,
    db: Session = Depends(get_db)
):

    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    return question

@router.put("/{question_id}")
def update_question(
    question_id: int,
    updated_question: QuestionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    question.subject_id = updated_question.subject_id
    question.question_text = updated_question.question_text
    question.option_a = updated_question.option_a
    question.option_b = updated_question.option_b
    question.option_c = updated_question.option_c
    question.option_d = updated_question.option_d
    question.correct_answer = updated_question.correct_answer

    db.commit()

    return {
        "message": "Question updated successfully"
    }

@router.delete("/{question_id}")
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    db.delete(question)
    db.commit()

    return {
        "message": "Question deleted successfully"
    }

@router.get("/subject/{subject_id}")
def get_questions_by_subject(
    subject_id: int,
    db: Session = Depends(get_db)
):

    questions = db.query(Question).filter(
        Question.subject_id == subject_id
    ).all()

    return questions

@router.get("/random/{subject_id}")
def random_questions(
    subject_id: int,
    db: Session = Depends(get_db)
):

    questions = db.query(Question).filter(
        Question.subject_id == subject_id
    ).all()

    if not questions:
        raise HTTPException(
            status_code=404,
            detail="No questions found"
        )

    return random.sample(
        questions,
        min(5, len(questions))
    )
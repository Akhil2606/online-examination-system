from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.subject import Subject
from app.schemas.subject import SubjectCreate
from app.models.result import Result
from app.core.permissions import admin_required

router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"]
)


@router.post("/")
def create_subject(
    subject: SubjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    existing_subject = db.query(Subject).filter(
        Subject.subject_name == subject.subject_name
    ).first()

    if existing_subject:
        raise HTTPException(
            status_code=400,
            detail="Subject already exists"
        )

    new_subject = Subject(
        subject_name=subject.subject_name
    )

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)

    return {
        "message": "Subject created successfully"
    }


@router.get("/")
def get_all_subjects(
    db: Session = Depends(get_db)
):

    subjects = db.query(Subject).all()

    return subjects

@router.get("/performance")
def subject_performance(
    db: Session = Depends(get_db)
):

    total_subjects = db.query(Subject).count()

    total_results = db.query(Result).count()

    return {
        "total_subjects": total_subjects,
        "total_results": total_results
    }


@router.get("/{subject_id}")
def get_subject_by_id(
    subject_id: int,
    db: Session = Depends(get_db)
):

    subject = db.query(Subject).filter(
        Subject.id == subject_id
    ).first()

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    return subject

@router.put("/{subject_id}")
def update_subject(
    subject_id: int,
    updated_subject: SubjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    subject = db.query(Subject).filter(
        Subject.id == subject_id
    ).first()

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    subject.subject_name = updated_subject.subject_name

    db.commit()

    return {
        "message": "Subject updated successfully"
    }


@router.delete("/{subject_id}")
def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    subject = db.query(Subject).filter(
        Subject.id == subject_id
    ).first()

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    db.delete(subject)
    db.commit()

    return {
        "message": "Subject deleted successfully"
    }


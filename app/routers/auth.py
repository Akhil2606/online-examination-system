from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from fastapi import Header
from app.utils.jwt_handler import verify_access_token
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserLogin
from app.core.security import verify_password
from app.utils.jwt_handler import create_access_token
from app.core.dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role_id=user.role_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    if not verify_password(
        form_data.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    access_token = create_access_token(
    {
        "sub": db_user.email,
        "user_id": db_user.id,
        "role_id": db_user.role_id
    }
)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(
    current_user=Depends(get_current_user)
):
    return current_user

@router.get("/me-test")
def me_test(authorization: str = Header()):

    token = authorization.replace("Bearer ", "")

    payload = verify_access_token(token)

    return payload
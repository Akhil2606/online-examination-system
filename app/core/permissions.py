from fastapi import Depends
from fastapi import HTTPException

from app.core.dependencies import get_current_user


def admin_required(
    current_user=Depends(get_current_user)
):

    if current_user["role_id"] != 1:
        raise HTTPException(
            status_code=403,
            detail="Admin Access Required"
        )

    return current_user
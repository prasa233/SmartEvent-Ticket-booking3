
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.dependencies import require_admin

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.put("/users/{user_id}/make-organizer")
def make_organizer(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    user.role = "ORGANIZER"
    db.commit()
    db.refresh(user)

    return {
        "message": "User promoted to organizer successfully",
        "user_id": user.id,
        "name": user.name,
        "role": user.role,
    }

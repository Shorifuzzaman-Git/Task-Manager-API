from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)


@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "is_verified": current_user.is_verified
    }
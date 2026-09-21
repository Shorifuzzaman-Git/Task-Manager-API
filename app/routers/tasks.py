from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse
from app.services.task_service import create_task


router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"]
)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_task(
        db=db,
        task_data=task_data,
        current_user=current_user
    )
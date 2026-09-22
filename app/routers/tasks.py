from fastapi import APIRouter, Depends, status,HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.task import (
    TaskCreate, 
    TaskResponse,
    TaskUpdate
)
from app.services.task_service import (
    create_task,
    get_user_tasks,
    get_task_by_id,
    update_task,
    delete_task
)

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

@router.get(
    "",
    response_model=list[TaskResponse]
)
def get_my_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_user_tasks(
        db=db,
        current_user=current_user
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse
)
def get_single_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = get_task_by_id(
        db=db,
        task_id=task_id,
        current_user=current_user
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse
)
def update_existing_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = update_task(
        db=db,
        task_id=task_id,
        task_data=task_data,
        current_user=current_user
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_existing_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    deleted = delete_task(
        db=db,
        task_id=task_id,
        current_user=current_user
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
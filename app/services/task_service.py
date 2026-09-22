from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate,TaskUpdate


def create_task(
    db: Session,
    task_data: TaskCreate,
    current_user: User
) -> Task:

    task = Task(
        title=task_data.title,
        description=task_data.description,
        status="pending",
        user_id=current_user.id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_user_tasks(
    db: Session,
    current_user: User
) -> list[Task]:

    tasks = (
        db.query(Task)
        .filter(Task.user_id == current_user.id)
        .order_by(Task.created_at.desc())
        .all()
    )

    return tasks


def get_task_by_id(
    db: Session,
    task_id: int,
    current_user: User
) -> Task | None:

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == current_user.id
        )
        .first()
    )

    return task


def update_task(
    db: Session,
    task_id: int,
    task_data: TaskUpdate,
    current_user: User
) -> Task | None:

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == current_user.id
        )
        .first()
    )

    if not task:
        return None

    if task_data.title is not None:
        task.title = task_data.title

    if task_data.description is not None:
        task.description = task_data.description

    if task_data.status is not None:
        task.status = task_data.status

    db.commit()
    db.refresh(task)

    return task

def delete_task(
    db: Session,
    task_id: int,
    current_user: User
) -> bool:

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == current_user.id
        )
        .first()
    )

    if not task:
        return False

    db.delete(task)
    db.commit()

    return True


from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate


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
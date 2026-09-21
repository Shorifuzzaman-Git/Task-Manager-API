from fastapi import FastAPI

from app.routers import auth,users,tasks


app = FastAPI(
    title="Task Manager API",
    description="A secure task management REST API",
    version="1.0.0"
)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)


@app.get("/")
def root():
    return {
        "message": "Task Manager API is running"
    }
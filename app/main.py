
from app.routers import task, user
from sqlalchemy.schema import CreateTable
from fastapi import FastAPI, Depends, HTTPException, status
from app.backend.db import engine, Base
from app.models import User, Task

app = FastAPI()
@app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager"}

app.include_router(task.router)
app.include_router(user.router)

Base.metadata.create_all(bind=engine)


print("SQL для User:")
print(CreateTable(User.__table__))
print("\nSQL для Task:")
print(CreateTable(Task.__table__))


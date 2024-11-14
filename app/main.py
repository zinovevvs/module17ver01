# from fastapi import FastAPI
# from app.routers import task, user
#
# app = FastAPI()
#
# @app.get("/")
# async def welcome():
#     return {"message": "Welcome to Taskmanager"}
#
# app.include_router(task.router)
# app.include_router(user.router)

from fastapi import FastAPI
from app.backend.db import engine, Base
from app.models import User, Task

app = FastAPI()

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

from sqlalchemy.schema import CreateTable
print("SQL для User:")
print(CreateTable(User.__table__))
print("\nSQL для Task:")
print(CreateTable(Task.__table__))

@app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager"}




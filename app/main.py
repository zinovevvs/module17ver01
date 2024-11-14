from sqlalchemy.orm import Session

from app.routers import task, user
from sqlalchemy.schema import CreateTable
from fastapi import FastAPI, Depends, HTTPException, status
from app.backend.db import engine, Base
from app.models import User, Task
from sqlalchemy import select, insert, update, delete
from app.backend.db import get_db
from app.schemas import CreateUser, UpdateUser

app = FastAPI()
@app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager"}

app.include_router(task.router)
app.include_router(user.router)

Base.metadata.create_all(bind=engine)


# print("SQL для User:")
# print(CreateTable(User.__table__))
# print("\nSQL для Task:")
# print(CreateTable(Task.__table__))
@app.get("/users/")
async def all_users(db: Session = Depends(get_db)):
    # Возвращает список всех пользователей
    users = db.execute(select(User)).scalars().all()
    return users

@app.get("/user/{user_id}")
async def user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return user

@app.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    existing_user = db.execute(select(User).where(User.username == user.username)).scalar_one_or_none()
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@app.put("/update/{user_id}")
async def update_user(user_id: int, user: UpdateUser, db: Session = Depends(get_db)):
    stmt = update(User).where(User.id == user_id).values(**user.dict())
    result = db.execute(stmt)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User was not found")
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}

@app.delete("/delete/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    stmt = delete(User).where(User.id == user_id)
    result = db.execute(stmt)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User was not found")
    return {'status_code': status.HTTP_204_NO_CONTENT, 'transaction': 'User deleted successfully!!'}




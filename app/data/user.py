from app.model.user import User, UserCreate, UserUpdate
from sqlalchemy.orm import Session
from app.data import crud

from fastapi import Depends, HTTPException
from db.sesssion import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user(id_user: int) -> User:
    db = next(get_db())
    db_user = crud.get_user(db=db, user_id=id_user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_user

def get_all(skip: int, limit: int, order_by: str, order_direction: str) -> list[User]:
    db = next(get_db())
    users = crud.get_all(db, skip, limit, order_by, order_direction)
    return users

def create_user(user: UserCreate) -> User:
    db = next(get_db())
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

def delete_user(user_id: int):
    db = next(get_db())
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is not None:
        crud.delete_user_by_id(db=db, user_id=user_id)
        raise HTTPException(status_code=200, detail="user deleted")
    else:
        raise HTTPException(status_code=404, detail="user not found")

def updata_user(user_id: int, user_update: UserUpdate, current_user: str) -> User:
    db = next(get_db())
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is not None:
        if current_user["sub"] != db_user.user_name:
            raise HTTPException(
                status_code=403, detail="Not authorized to update this user"
            )
        crud.update_user(db=db, user_id=user_id, user_update=user_update)
        raise HTTPException(status_code=200, detail="user changed")
    else:
        raise HTTPException(status_code=404, detail="user not found")
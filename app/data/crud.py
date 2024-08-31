from sqlalchemy.orm import Session
from db.model import user as UserModel
from schemas import user as SchemasUser
from app.core import security
from sqlalchemy import asc, desc


# get user by id
def get_user(db: Session, user_id: int):
    return db.query(UserModel.User).filter(UserModel.User.id == user_id).first()


# get user by user_name
def get_user_by_user_name(db: Session, user_name: str):
    return (
        db.query(UserModel.User).filter(UserModel.User.user_name == user_name).first()
    )


# get user by email
def get_user_by_email(db: Session, email: str):
    return db.query(UserModel.User).filter(UserModel.User.email == email).first()


# get all users
def get_all(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    order_by: str = "id",
    order_direction: str = "asc",
):
    if limit < 0:
        limit = 100
    if skip < 0:
        skip = 0
    order_func = asc if order_direction == "asc" else desc
    query = (
        db.query(UserModel.User)
        .order_by(order_func(getattr(UserModel.User, order_by)))
        .offset(skip)
        .limit(limit)
    )
    return query.all()


# cretae user
def create_user(db: Session, user: SchemasUser.UserCreate):
    hashed_password = security.hash_password(user.password)
    db_user = UserModel.User(
        user_name=user.user_name, email=user.email, password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# delete user by id
def delete_user_by_id(db: Session, user_id: int):
    db_user = db.query(UserModel.User).filter(UserModel.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


# update user
def update_user(db: Session, user_id: int, user_update: SchemasUser.UserUpdate):
    db_user = db.query(UserModel.User).filter(UserModel.User.id == user_id).first()
    if db_user:
        for key, value in user_update.model_dump().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def authenticate_user(db, user_name: str, password: str):
    user = get_user_by_user_name(db=db, user_name=user_name)
    if not user:
        return False
    if not security.hash_verify(password=password, hashe_pass=user.password):
        return False
    return user

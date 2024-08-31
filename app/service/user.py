from app.model.user import User, UserCreate, UserUpdate
import app.data.user as data

def get_user(id_user: int) -> User | None:
    return data.get_user(id_user)

def get_all(skip: int, limit: int, order_by: str, order_direction: str) -> list[User]:
    return data.get_all(skip, limit, order_by, order_direction)

def create_user(user: UserCreate) -> User:
    return data.create_user(user=user)

def delete_user(user_id: int):
    return data.delete_user(user_id)

def updata_user(user_id: int, user_update: UserUpdate, current_user: str) -> User:
    return data.updata_user(user_id, user_update, current_user)
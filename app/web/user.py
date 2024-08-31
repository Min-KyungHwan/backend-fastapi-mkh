from fastapi import APIRouter, HTTPException, Depends
from schemas import user as SchemasUser
from app.model.user import User, UserCreate, UserUpdate
import app.service.user as service
from sqlalchemy.orm import Session
from db.sesssion import SessionLocal, engine
from app.data import crud
from fastapi.security import OAuth2PasswordBearer
from app.core.jwt_config import create_access_token, decode_token, get_current_user1
import jwt
from typing import Annotated
from app.data.crud import get_user_by_user_name
from fastapi import Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)

from schemas.user import TokenData
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel, ValidationError


SECRET_KEY = "e6ec9b1b3cff28c775d63af5f1be939fdf351054ec53543fbba2cd147a21665e"
ALGORITHM = "HS256"

router = APIRouter(prefix="/user")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="user/token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    user = get_user_by_user_name(db, user_name=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


@router.get("/{user_id}")
def read_user(id_user: int, current_user: str = Depends(get_current_user)) -> User:
    return service.get_user(id_user)


@router.get("/")
def read_users(
    skip: int = 0,
    limit: int = 100,
    order_by: str = "id",
    order_direction: str = "desc",
) -> list[User]:
    return service.get_all(skip, limit, order_by, order_direction)


@router.post("/create")
def create_user(user: UserCreate) -> User:
    return service.create_user(user)


@router.delete("/delete/{user_id}")
def delete_user(user_id: int):
    return service.delete_user(user_id)


@router.put("/update/{user_id}")
def updata_user(user_id: int, user_update: UserUpdate, current_user: str = Depends(get_current_user1)) -> User:
    return service.updata_user(user_id, user_update, current_user)


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user.user_name, "scopes": form_data.scopes},
    )
    return SchemasUser.Token(access_token=access_token, token_type="bearer")
    # return User.Token(access_token=access_token, token_type="bearer")

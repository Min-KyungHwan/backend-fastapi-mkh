import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
from typing import Optional
from datetime import datetime, timedelta, timezone
from typing import Annotated
from app.data.crud import get_user_by_user_name
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from sqlalchemy.orm import Session
from schemas.user import TokenData
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    data_encode = data.copy()
    encode = jwt.encode(data_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode


def decode_token(token: str):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return data
    except PyJWTError:
        raise None


def get_current_user1(token: str = Depends(oauth2_scheme)):
    accept = decode_token(token=token)
    if accept is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return accept



from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserCreate(BaseModel):
    user_name: str = Field(
        ...,
        min_length=3,
        max_length=255,
        example="example_user",
        description="The username of the user",
    )
    email: EmailStr = Field(
        ...,
        min_length=10,
        max_length=255,
        example="example@example.com",
        description="The email address of the user",
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=255,
        example="strong_password123",
        description="The password for the user account",
    )


class UserUpdate(BaseModel):
    user_name: str = Field(
        ...,
        min_length=3,
        max_length=255,
        example="example_user",
        description="The username of the user",
    )
    email: EmailStr = Field(
        ...,
        min_length=10,
        max_length=255,
        example="example@example.com",
        description="The email address of the user",
    )


class User(BaseModel):
    id: int
    user_name: str
    email: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    user_name : str
    password : str
class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []

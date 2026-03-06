from typing import Optional, Annotated
import string
from backend.app.models.core import DateTimeModelMixin, CoreModel, IdModelMixin
from pydantic import EmailStr, field_validator, Field
import re


def validate_username(username: str):
    allowed = string.ascii_letters + string.digits + "-" + "_"
    assert all(char in allowed for char in username), "Invalid char in username"
    assert len(username) > 3
    return username


def validate_password(password: str):
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain an uppercase letter")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain a number")
    return password


class UserBase(CoreModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    email_verified: bool = False
    is_active: bool = False
    is_superuser: bool = False


class UserCreate(CoreModel):
    username: str
    email: EmailStr
    password: Annotated[str, Field(min_length=7, max_length=200)]

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_password(password=v)

    @field_validator("username", mode="before")
    @classmethod
    def validate_username(cls, username: str) -> str:
        return validate_username(username=username)


class UserUpdate(CoreModel):
    """
    Users are allowed to update their email and/or username
    """

    email: Optional[EmailStr] = None
    username: Optional[str] = None

    @field_validator("username", mode="before")
    @classmethod
    def username_is_valid(cls, username: str) -> str:
        return validate_username(username)


class UserPasswordUpdate(CoreModel):
    password: Annotated[str, Field(min_length=7, max_length=200)]

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        return validate_password(v)


class UserInDB(IdModelMixin, DateTimeModelMixin, UserBase):
    """
    Add in id, created_at, updated_at, and user's password and salt
    """

    password: Annotated[str, Field(min_length=7, max_length=200)]

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_password(password=v)


class UserPublic(IdModelMixin, DateTimeModelMixin, UserBase):
    pass

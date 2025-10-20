from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

from crud import users
from database import SessionDep
from schemas.users import (Token, UserBase, UserCreate, UserModifyPassword,
                           UserWithRole)

ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

router = APIRouter()


@router.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> Token:
    user = users.authenticate_user(form_data, session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = users.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=UserWithRole)
def read_users_me(
    current_user: Annotated[UserBase, Depends(users.get_current_user)],
):
    return current_user


@router.post("/users/", response_model=UserWithRole)
def create_user(user: UserCreate, session: SessionDep):
    db_user = users.get_user_by_email(session, user.email)
    if db_user:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "The email already exists")

    return users.create_user(session, user)


@router.delete("/users/{user_uuid}", response_model=UserWithRole)
def delete_user(session: SessionDep, user_uuid: str):
    db_user = users.get_user_by_uuid(session, user_uuid)

    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    return users.delete_user(session, user_uuid)


@router.patch("/users/{user_uuid}/role", response_model=UserWithRole)
def change_user_role(session: SessionDep, user_uuid: str, new_role: str):

    db_user = users.get_user_by_uuid(session, user_uuid)

    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    return users.change_role(session, user_uuid, new_role)


@router.patch("/users/{user_uuid}/email")
def change_user_email(session: SessionDep, user_uuid: str, new_email: str):
    db_user = users.get_user_by_uuid(session, user_uuid)

    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    try:
        return users.change_email(session, user_uuid, new_email)
    except IntegrityError:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "Email already exists")


@router.patch("/users/{user_uuid}/password")
def change_user_password(
    user_modify_password: UserModifyPassword, user_uuid: str, session: SessionDep
):
    db_user = users.get_user_by_uuid(session, user_uuid)

    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    return users.change_password(session, user_uuid, user_modify_password.new_password)

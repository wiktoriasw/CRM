from datetime import timedelta
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

from configuration import ACCESS_TOKEN_EXPIRE_MINUTES
from crud import users
from db import SessionDep
from dependencies.users import get_admin_user, get_current_user
from models.users import User as UserModel
from schemas.users import (Token, UserBase, UserCreate, UserModifyEmail,
                           UserModifyPassword, UserModifyRole, UserWithRole)
from schemas.utils import Status

router = APIRouter()


def parse_user(user: UserModel) -> UserModel:
    return {
        **user.__dict__,
        "role": user.role.name,
    }


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
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    return parse_user(current_user)


@router.get("/users", response_model=List[UserWithRole])
def get_users(session: SessionDep, _: Annotated[UserBase, Depends(get_admin_user)]):
    return map(parse_user, users.get_users(session))


@router.post("/users/", response_model=UserWithRole)
def create_user(user: UserCreate, session: SessionDep):

    db_user = users.get_user_by_email(session, user.email)
    if db_user:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "The email already exists")

    return parse_user(users.create_user(session, user))


@router.delete("/users/{user_uuid}", response_model=UserWithRole)  # admin
def delete_user(
    session: SessionDep,
    current_user: Annotated[UserBase, Depends(get_current_user)],
    user_uuid: str,
):

    db_user = users.get_user_by_uuid(session, user_uuid)

    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    return parse_user(users.delete_user(session, current_user.user_uuid))


@router.patch("/users/{user_uuid}/role", response_model=UserWithRole)
def change_user_role(
    user: UserModifyRole,
    current_user: Annotated[UserBase, Depends(get_admin_user)],
    session: SessionDep,
    user_uuid: str,
):

    db_user = users.get_user_by_uuid(session, user_uuid)

    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    if current_user.user_uuid == user_uuid:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Admin can't change their own role",
        )

    return parse_user(users.change_role(session, user_uuid, user.new_role))


@router.patch("/users/me/email", response_model=Status)
def change_user_email(
    user: UserModifyEmail,
    current_user: Annotated[UserBase, Depends(get_current_user)],
    session: SessionDep,
):
    try:
        users.change_email(session, current_user.user_uuid, user.new_email)
        return {"status": "ok"}
    except IntegrityError:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "Email already exists")


@router.patch("/users/me/password", response_model=Status)
def change_user_password(
    user_modify_password: UserModifyPassword,
    current_user: Annotated[UserBase, Depends(get_current_user)],
    session: SessionDep,
):
    db_user = users.get_user_by_uuid(session, current_user.user_uuid)

    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    if not users.verify_password(
        user_modify_password.old_password, db_user.hashed_password
    ):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Incorrect current password.")

    users.change_password(session, current_user.user_uuid, user_modify_password.new_password)

    return {"status": "Ok"}

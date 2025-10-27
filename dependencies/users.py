from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from configuration import ALGORITHM, SECRET_KEY
from crud.users import get_user_by_email
from db import SessionDep
from dependencies.oauth import oauth2_scheme
from models.users import UserRole
from schemas.users import TokenData, User, UserBase


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user_by_email(session, token_data.username)

    if user is None:
        raise credentials_exception

    return user


def get_admin_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="You don't have permissions"
        )

    return current_user


def get_admin_or_guide_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.role not in (UserRole.admin, UserRole.guide):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You don't have permissions")


UserDep = Annotated[UserBase, Depends(get_current_user)]

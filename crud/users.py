from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pwdlib import PasswordHash
from sqlalchemy import func
from sqlalchemy.orm import Session

import models
from database import SessionDep
from schemas.users import TokenData, UserCreate

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def _get_not_deleted_user(db: Session):
    return db.query(models.User).filter(models.User.deleted_at == None)


def get_user_by_email(db, email: str):
    return _get_not_deleted_user(db).filter(models.User.email == email).first()


def get_user_by_uuid(db, user_uuid: str):
    return _get_not_deleted_user(db).filter(models.User.user_uuid == user_uuid).first()


def create_user(db, user: UserCreate):
    hashed_pw = get_password_hash(user.password)
    user = models.User(
        email=user.email,
        hashed_password=hashed_pw,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def delete_user(db, user_uuid: str):
    db_user = get_user_by_uuid(db, user_uuid)
    db_user.deleted_at = func.now()
    db.commit()
    db.refresh(db_user)

    return db_user


def change_role(db, user_uuid: str, new_role: str):
    db_user = get_user_by_uuid(db, user_uuid)
    db_user.role = new_role
    db.commit()
    db.refresh(db_user)

    return db_user


def change_password(db, user_uuid: str, new_password: str):
    db_user = get_user_by_uuid(db, user_uuid)

    db_user.hashed_password = get_password_hash(new_password)
    db.commit()
    db.refresh(db_user)

    return db_user


def change_email(db, user_uuid: str, new_email: str):
    db_user = get_user_by_uuid(db, user_uuid)

    db_user.email = new_email
    db.commit()

    return db_user


def authenticate_user(form_data: OAuth2PasswordRequestForm, db: Session):
    db_user = get_user_by_email(db, form_data.username)

    if not db_user:
        return False

    if not verify_password(form_data.password, db_user.hashed_password):
        return False

    return db_user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


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

from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pwdlib import PasswordHash
from sqlalchemy import func
from sqlalchemy.orm import Session

from configuration import ALGORITHM, SECRET_KEY
from models import users
from schemas.users import UserCreate

password_hash = PasswordHash.recommended()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def _get_not_deleted_users(db: Session):
    return db.query(users.User).filter(users.User.deleted_at == None)


def get_users(db: Session):
    return _get_not_deleted_users(db).all()


def get_user_by_email(db, email: str):
    return _get_not_deleted_users(db).filter(users.User.email == email).first()


def get_user_by_uuid(db, user_uuid: str):
    return _get_not_deleted_users(db).filter(users.User.user_uuid == user_uuid).first()


def create_user(db, user: UserCreate):
    hashed_pw = get_password_hash(user.password)
    user = users.User(
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


def change_role(db, user_uuid: str, new_role: users.UserRole):
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

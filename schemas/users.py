from sqlmodel import SQLModel


class User(SQLModel):
    user_uuid: str
    role: str


class UserBase(SQLModel):
    email: str


class UserWithRole(UserBase):
    role: str


class UserModifyEmail(SQLModel):
    new_email: str


class UserModifyRole(SQLModel):
    new_role: str


class UserModifyPassword(SQLModel):
    old_password: str
    new_password: str


class UserCreate(UserBase):
    password: str


class UserModify(UserCreate):
    pass


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None

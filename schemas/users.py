from sqlmodel import SQLModel


class UserBase(SQLModel):
    email: str


class UserWithRole(UserBase):
    role: str


class UserModifyPassword(SQLModel):
    old_password: str
    new_password: str


class UserInDB(UserBase):
    hashed_password: str


class UserCreate(UserBase):
    password: str


class UserModify(UserCreate):
    pass


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None

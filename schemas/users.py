
from sqlmodel import SQLModel


class User(SQLModel):
    email: str
    role: str

class User(SQLModel):
    username: str
    email: str
    full_name: str

class UserInDB(User):
    hashed_password: str


class UserCreate(SQLModel):
    email: str


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None




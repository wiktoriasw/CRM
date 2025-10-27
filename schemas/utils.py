from sqlmodel import SQLModel


class Status(SQLModel):
    status: str

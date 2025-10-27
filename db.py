from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlmodel import create_engine

from models.utils import Base as SQLModel

postgresql_url = "postgresql://postgres:postgres@localhost:5432/postgres"

engine = create_engine(postgresql_url)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

import uuid

from sqlalchemy.orm import declarative_base

Base = declarative_base()


def get_uuid4():
    return str(uuid.uuid4())

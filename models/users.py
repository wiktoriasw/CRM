import enum

from sqlalchemy import Column, Enum, String
from sqlalchemy.orm import relationship

from models.mixin import TimestampMixin
from models.utils import Base, get_uuid4


class UserRole(enum.Enum):
    user = 1
    admin = 2
    guide = 3


class UserGender(enum.Enum):
    female = 1
    male = 2
    unknown = 3


class User(TimestampMixin, Base):
    __tablename__ = "user"

    user_uuid = Column(String, primary_key=True, default=get_uuid4)
    email = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)

    payments = relationship("Payment", back_populates="user")
    news = relationship("News", back_populates="user")
    participants = relationship(
        "Participant",
        back_populates="user",
        foreign_keys="Participant.user_uuid",
    )

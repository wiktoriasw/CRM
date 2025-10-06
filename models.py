import enum
import uuid

from sqlalchemy import (Column, Date, DateTime, Enum, ForeignKey, Integer,
                        String, Table)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.types import DECIMAL

Base = declarative_base()


def get_uuid4():
    return str(uuid.uuid4())


class UserRole(enum.Enum):
    user = 1
    admin = 2
    guide = 3


class UserGender(enum.Enum):
    female = 1
    male = 2
    unknown = 3


class User(Base):
    __tablename__ = "user"

    user_uuid = Column(String, primary_key=True, default=get_uuid4)
    email = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)

    payments = relationship("Payment", back_populates="user")
    news = relationship("News", back_populates="user")
    participants = relationship("Participant", back_populates="user")


participants_payments_association_table = Table(
    "participants_payments",
    Base.metadata,
    Column(
        "participant_uuid", ForeignKey("participant.participant_uuid"), primary_key=True
    ),
    Column("payment_uuid", ForeignKey("payment.payment_uuid"), primary_key=True),
)


class Participant(Base):
    __tablename__ = "participant"

    participant_uuid = Column(String, primary_key=True, default=get_uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    gender = Column(Enum(UserGender), nullable=False)
    birth_date = Column(Date, nullable=False)
    trip_uuid = Column(String, ForeignKey("trip.trip_uuid"), nullable=False)
    user_uuid = Column(String, ForeignKey("user.user_uuid"), nullable=False)
    chosen_meet_point = Column(String)
    group_code = Column(String)
    comments = Column(String)

    trip = relationship("Trip", back_populates="participants")
    user = relationship("User", back_populates="participants")
    payments = relationship(
        "Payment",
        secondary=participants_payments_association_table,
        back_populates="participants",
    )


trips_surveys = Table(
    "trips_surveys",
    Base.metadata,
    Column("trip_uuid", ForeignKey("trip.trip_uuid"), primary_key=True),
    Column("survey_uuid", ForeignKey("survey.survey_uuid"), primary_key=True),
)


class Trip(Base):
    __tablename__ = "trip"

    trip_uuid = Column(String, primary_key=True, default=get_uuid4)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    payment_schedule = Column(String, nullable=False)
    meet_points = Column(ARRAY(String), nullable=False)
    background_photo = Column(String, nullable=False)
    deleted_at = Column(Date, nullable=True)
    user_uuid = Column(String, ForeignKey("user.user_uuid"), nullable=False)

    participants = relationship("Participant", back_populates="trip")
    insurance_policy = relationship("InsurancePolicy", back_populates="trip")
    payments = relationship("Payment", back_populates="trip")
    news = relationship("News", back_populates="trip")
    surveys = relationship("Survey", secondary=trips_surveys, back_populates="trips")


class Payment(Base):
    __tablename__ = "payment"

    payment_uuid = Column(String, primary_key=True, default=get_uuid4)
    user_uuid = Column(String, ForeignKey("user.user_uuid"), nullable=False)
    trip_uuid = Column(String, ForeignKey("trip.trip_uuid"), nullable=False)
    date = Column(Date, nullable=False)
    amount = Column(DECIMAL(7, 2), nullable=False)

    user = relationship("User", back_populates="payments")
    trip = relationship("Trip", back_populates="payments")
    participants = relationship(
        "Participant",
        secondary=participants_payments_association_table,
        back_populates="payments",
    )


class Survey(Base):
    __tablename__ = "survey"

    survey_uuid = Column(String, primary_key=True, default=get_uuid4)
    user_uuid = Column(String, ForeignKey("user.user_uuid"), nullable=False)
    trip_uuid = Column(String, ForeignKey("trip.trip_uuid"), nullable=False)
    questions = Column(JSONB, nullable=False)

    trips = relationship("Trip", secondary=trips_surveys, back_populates="surveys")


class Answer(Base):
    __tablename__ = "answer"

    answer_uuid = Column(String, primary_key=True, default=get_uuid4)
    user_uuid = Column(String, ForeignKey("user.user_uuid"), nullable=False)
    answers = Column(ARRAY(String), nullable=False)
    survey_uuid = Column(String, ForeignKey("survey.survey_uuid"), nullable=False)


class InsurancePolicy(Base):
    __tablename__ = "insurance_policy"

    policy_uuid = Column(String, primary_key=True, default=get_uuid4)
    policy_number = Column(String, nullable=False)
    company = Column(String, nullable=False)
    trip_uuid = Column(String, ForeignKey("trip.trip_uuid"), nullable=False)

    trip = relationship("Trip", back_populates="insurance_policy")


class News(Base):
    __tablename__ = "news"
    news_uuid = Column(String, primary_key=True, default=get_uuid4)
    user_uuid = Column(String, ForeignKey("user.user_uuid"), nullable=False)
    trip_uuid = Column(String, ForeignKey("trip.trip_uuid"), nullable=False)
    content = Column(String, nullable=False)
    title = Column(String, nullable=False)
    publication_date = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="news")
    trip = relationship("Trip", back_populates="news")

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Enum, Date
# from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.types import DECIMAL

import enum

from .database import Base

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

    user_uuid = Column(String, primary_key=True, default=utils.get_uuid4)
    email = Column(String(50), unique=True, nullable=False) 
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)

    # payments = relationship("Payment", back_populates="user")
    # news = relationship("News", back_populates="author") 


class Participant(Base):
    __tablename__ = "participant"

    participant_uuid = Column(String, primary_key=True, default=utils.get_uuid4)
    name = Column(String, nullable=False) 
    surname = Column(String, nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    gender = Column(Enum(UserGender), nullable=False)
    birth_date = Column(Date, nullable=False)
    trip_uuid = Column(Integer, ForeignKey("trips.trip_uuid"), nullable=False)
    chosen_meet_point = Column(String)
    group_code = Column(String)
    comments = Column(String)
    
    # trips = relationship("Trip", back_populates="participant")  


class Trip(Base):
    __tablename__ = "trip"

    trip_uuid = Column(String, primary_key=True, default=utils.get_uuid4)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    start_date =Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    payment_schedule = Column(String, nullable=False)
    meet_points = Column(ARRAY(String), nullable=False)
    background_photo = Column(String, nullable=False)

    # participant = relationship("Participant", back_populates="trips")

class Payment(Base):
    __tablename__ = "payment"

    payment_uuid = Column(String, primary_key=True, default=utils.get_uuid4)
    user_uuid = Column(String, ForeignKey("users.user_uuid"), nullable=False)
    date = Column(Date, nullable=False)
    amount = Column(DECIMAL(7,2), nullable=False)

    # user = relationship("User", back_populates="payments")

class Survey(Base):
    __tablename__ = "survey"

    survey_uuid = Column(Integer, primary_key=True, default=utils.get_uuid4)
    user_uuid = Column(String, ForeignKey("users.user_uuid"), nullable=False)
    trip_uuid = Column(Integer, ForeignKey("trips.trip_uuid"), nullable=False)
    questions = Column(JSONB, nullable=False)


class Answer(Base):
    __tablename__ = "answer"

    answer_uuid = Column(Integer, primary_key=True, default=utils.get_uuid4)
    user_uuid = Column(String, ForeignKey("users.user_uuid"), nullable=False)
    answers = Column(ARRAY(String), nullable=False)
    survey_uuid = Column(String, ForeignKey("survey.survey_uuid"), nullable=False)
    

class InsurancePolicy(Base):
    __tablename__ = "insurance_policy"

    policy_uuid = Column(String, primary_key=True, default=utils.get_uuid4)
    policy_number = Column(String, nullable=False)
    company = Column(String, nullable=False)
    trip_uuid = Column(String, ForeignKey("trips.trip_uuid"), nullable=False)


class News(Base):
    __tablename__ = "news"
    news_uuid = Column(String, primary_key=True, default=utils.get_uuid4)
    user_uuid = Column(Integer, ForeignKey("users.user_uuid"), nullable=False)
    content = Column(String, nullable=False)
    title = Column(String, nullable=False)
    publication_date = Column(DateTime, nullable=False) 

    #   = relationship("User", back_populates="news")

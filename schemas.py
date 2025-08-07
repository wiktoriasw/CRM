from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    uuid = Column(String, default=utils.get_uuid4)
    email = Column(String(50), unique=True)
    hashed_password = Column(String)
    role = Column(String, default="user")

    payments = relationship("Payment", back_populates="user")
    news = relationship("News", back_populates="author") 


class Pax(Base):
    __tablename__ = "pax"

    pax_id = Column(Integer, primary_key=True)
    uuid = Column(String, default=utils.get_uuid4)
    name = Column(String)
    surname = Column(String)
    email = Column(String(50),unique = True)
    phone = Column(String(20))
    gender = Column(String)
    birth_date = Column(DateTime)
    trip_id = Column(Integer, ForeignKey("trips.trip_id"))
    chosen_meet_point = Column(String)
    group_code = Column(String)
    comments = Column(String)
    
    trips = relationship("Trips", back_populates="pax")  


class Trip(Base):
    __tablename__ = "trips"

    trip_id = Column(Integer, primary_key=True)
    trip_uuid = Column(String, default=utils.get_uuid4)
    name = Column(String)
    category = Column(String)
    start_date =Column(DateTime)
    end_date = Column(DateTime)
    description = Column(String)
    payment_schedule = Column(String)
    meet_point = Column(String)
    background_photo = Column(String)

    pax = relationship("Pax", back_populates="trips")

class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True)
    who_payed = Column(Integer, ForeignKey("users.user_id"))
    date = Column(DateTime)
    amount = Column( ) #float

    user = relationship("User", back_populates="payments")

class Survey(Base):
    __tablename__ = "surveys"

    surveys_id = Column(Integer, primary_key=True)
    author = Column(String)
    trip_id = Column(Integer, ForeignKey("trips.trip_id"))


class Answers(Base):
    __tablename__ = "answers"

    answer_id = Column(Integer, primary_key=True)
    questions = Column(String)
    answers = Column(String)
    

class InsurancePolicy(Base):
    __tablename__ = "insurance"

    policy_id = Column(Integer, primary_key=True)
    number = Column(String)
    company = Column(String)
    for_trip =  Column(Integer, ForeignKey("trips.trip_id"))


class News(Base):
    __tablename__ = "news"
    news_id = Column(Integer, primary_key=True)
    news_author = Column(Integer, ForeignKey("users.user_id"))
    description = Column(String)
    publication_date = Column(DateTime) 

    author = relationship("User", back_populates="news")

from models.associate_tables import trips_surveys
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from models.utils import Base, get_uuid4


class Survey(Base):
    __tablename__ = "survey"

    survey_uuid = Column(String, primary_key=True, default=get_uuid4)
    user_uuid = Column(String, ForeignKey("user.user_uuid"), nullable=False)
    trip_uuid = Column(String, ForeignKey("trip.trip_uuid"), nullable=False)
    questions = Column(JSONB, nullable=False)

    trips = relationship("Trip", secondary=trips_surveys, back_populates="surveys")

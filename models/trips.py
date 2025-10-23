from sqlalchemy import Column, Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from models.associate_tables import trips_surveys
from models.mixin import AuditUserMixin, TimestampMixin
from models.utils import Base, get_uuid4

import models.payments
import models.news
import models.insurance_policy
import models.surveys

class Trip(TimestampMixin, AuditUserMixin, Base):
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
    user_uuid = Column(String, ForeignKey("user.user_uuid"), nullable=False)

    participants = relationship("Participant", back_populates="trip")
    insurance_policy = relationship("InsurancePolicy", back_populates="trip")
    payments = relationship("Payment", back_populates="trip")
    news = relationship("News", back_populates="trip")
    surveys = relationship("Survey", secondary=trips_surveys, back_populates="trips")

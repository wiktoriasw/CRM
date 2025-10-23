from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from models.utils import Base, get_uuid4


class InsurancePolicy(Base):
    __tablename__ = "insurance_policy"

    policy_uuid = Column(String, primary_key=True, default=get_uuid4)
    policy_number = Column(String, nullable=False)
    company = Column(String, nullable=False)
    trip_uuid = Column(String, ForeignKey("trip.trip_uuid"), nullable=False)

    trip = relationship("Trip", back_populates="insurance_policy")

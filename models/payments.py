from models.associate_tables import participants_payments_association_table
from sqlalchemy import Column, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import DECIMAL
from models.utils import Base, get_uuid4


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

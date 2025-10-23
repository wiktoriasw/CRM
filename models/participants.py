from sqlalchemy import Column, Date, Enum, ForeignKey, String
from sqlalchemy.orm import relationship

from models.associate_tables import participants_payments_association_table
from models.mixin import AuditUserMixin, TimestampMixin
from models.users import UserGender
from models.utils import Base, get_uuid4


class Participant(TimestampMixin, AuditUserMixin, Base):
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
    user = relationship("User", back_populates="participants", foreign_keys=[user_uuid])
    payments = relationship(
        "Payment",
        secondary=participants_payments_association_table,
        back_populates="participants",
    )

from sqlalchemy import Column, ForeignKey, Table

from models.utils import Base

participants_payments_association_table = Table(
    "participants_payments",
    Base.metadata,
    Column(
        "participant_uuid", ForeignKey("participant.participant_uuid"), primary_key=True
    ),
    Column("payment_uuid", ForeignKey("payment.payment_uuid"), primary_key=True),
)


trips_surveys = Table(
    "trips_surveys",
    Base.metadata,
    Column("trip_uuid", ForeignKey("trip.trip_uuid"), primary_key=True),
    Column("survey_uuid", ForeignKey("survey.survey_uuid"), primary_key=True),
)

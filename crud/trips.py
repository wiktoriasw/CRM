from sqlalchemy.orm import Session
from datetime import date

import models
import schemas

def get_trip(db: Session, trip_uuid: str):
    return db.query(models.Trip).filter(models.Trip.trip_uuid==trip_uuid).first()


def create_trip(db: Session, trip: schemas.TripCreate):

    db_trip = models.Trip(**trip.model_dump())
    # db_trip.organizer_uuid = user_uuid
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)

    return db_trip


def modify_trip(db: Session, trip_modify: schemas.TripModify, trip_uuid: str):
    db_trip = db.query(models.Trip).filter(models.Trip.trip_uuid==trip_uuid).first()

    update_data = {
        k: v
        for k, v in trip_modify.model_dump(exclude_unset=True).items()
        if v is not None
    }

    if update_data:
        for key, value in update_data.items():
            setattr(db_trip, key, value)
        db.commit()

    return db_trip


def delete_trip(db:Session, trip_uuid: str):
    db_trip = db.query(models.Trip).filter(models.Trip.trip_uuid==trip_uuid).first()
    db_trip.deleted_at = date.today()
    db.commit()
    db.refresh(db_trip)

    return db_trip


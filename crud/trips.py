from datetime import datetime

from sqlalchemy.orm import Session

import models
import schemas


def get_trip(db: Session, trip_uuid: str):
    return db.query(models.Trip).filter(models.Trip.trip_uuid == trip_uuid).first()


def trips_with_filters(
    db: Session,
    end_date: datetime,
    start_date: datetime | None = None,
    q: str | None = None,
    category: str | None = None,
    limit: int = 3,
    offset: int = 0,
):

    query = db.query(models.Trip).filter(models.Trip.deleted_at == None)

    if q:
        query = query.filter(
            (models.Trip.name.ilike("%" + q + "%"))
            | (models.Trip.description.ilike("%" + q + "%"))
        )

    effective_end_date = end_date or datetime.now()
    if start_date:
        query = query.filter(models.Trip.start_date >= start_date).filter(
            models.Trip.end_date <= effective_end_date
        )

    if category:
        query = query.filter(models.Trip.category == category)

    if limit > 5:
        limit = 5

    query = query.limit(limit).offset(offset)

    db_trips = query.all()

    return db_trips


def get_not_deleted_trip(db: Session, trip_uuid: str):
    return (
        db.query(models.Trip)
        .filter(models.Trip.trip_uuid == trip_uuid)
        .filter(models.Trip.deleted_at == None)
        .first()
    )


def get_not_deleted_trips(db: Session):
    return db.query(models.Trip).filter(models.Trip.deleted_at == None)


def create_trip(db: Session, trip: schemas.TripCreate, user_uuid: str):

    db_trip = models.Trip(**trip.model_dump())
    db_trip.user_uuid = user_uuid
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)

    return db_trip


def modify_trip(db: Session, trip_modify: schemas.TripModify, trip_uuid: str):
    db_trip = db.query(models.Trip).filter(models.Trip.trip_uuid == trip_uuid).first()

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


def delete_trip(db: Session, trip_uuid: str, user_uuid: str):
    db_trip = db.query(models.Trip).filter(models.Trip.trip_uuid == trip_uuid).first()
    db_trip.user_uuid = user_uuid
    db_trip.deleted_at = datetime.today()
    db.commit()
    db.refresh(db_trip)

    return db_trip

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

import models
from schemas.trips import TripCreate, TripModify


def _get_not_deleted_trips(db: Session):
    return db.query(models.Trip).filter(models.Trip.deleted_at == None)


def get_trip(db: Session, trip_uuid: str):
    return _get_not_deleted_trips(db).filter(models.Trip.trip_uuid == trip_uuid).first()


def trips_with_filters(
    db: Session,
    from_start_date: datetime | None = None,
    to_start_date: datetime | None = None,
    q: str | None = None,
    category: str | None = None,
    limit: int = 3,
    offset: int = 0,
):

    query = _get_not_deleted_trips(db)

    if q:
        query = query.filter(
            (models.Trip.name.ilike("%" + q + "%"))
            | (models.Trip.description.ilike("%" + q + "%"))
        )

    if from_start_date:
        query = query.filter(models.Trip.start_date >= from_start_date)

    if to_start_date:
        query = query.filter(models.Trip.start_date <= to_start_date)

    if category:
        query = query.filter(models.Trip.category == category)

    query = query.limit(limit).offset(offset)

    db_trips = query.all()

    return db_trips


def create_trip(db: Session, trip: TripCreate, user_uuid: str):

    db_trip = models.Trip(**trip.model_dump())
    db_trip.user_uuid = user_uuid
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)

    return db_trip


def modify_trip(
    db: Session, trip_modify: TripModify, trip_uuid: str, user_uuid: str
):
    db_trip = get_trip(db, trip_uuid)

    update_data = {
        k: v
        for k, v in trip_modify.model_dump(exclude_unset=True).items()
        if v is not None
    }

    if update_data:
        for key, value in update_data.items():
            setattr(db_trip, key, value)

        db_trip.updated_by = user_uuid
        db.commit()

    return db_trip


def delete_trip(db: Session, trip_uuid: str, user_uuid: str):
    db_trip = get_trip(db, trip_uuid)
    db_trip.deleted_by = user_uuid
    db_trip.deleted_at = func.now()
    db.commit()
    db.refresh(db_trip)

    return db_trip

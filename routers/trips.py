from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, status

import models
from crud import trips
from database import SessionDep
from schemas import TripBase, TripCreate, TripModify

# from sqlalchemy import or_

router = APIRouter(prefix="/trips")
user_uuid = "576590e1-3f56-4a0a-aec5-5d84a319988f"


@router.get("/count")
def get_trips_count(session: SessionDep):
    db_trips = session.query(models.Trip).count()
    return db_trips


@router.get("/", response_model=List[TripBase])
def get_trips(
    session: SessionDep,
    q: str | None = None,
    category: str | None = None,
    limit: int = 3,
    offset: int = 0,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
):

    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Start date cannot be after end date"
        )

    return trips.trips_with_filters(
        session, end_date, start_date, q, category, limit, offset
    )


@router.get("/{trip_uuid}", response_model=TripBase)
def get_trip(trip_uuid: str, session: SessionDep):

    db_trip = trips.get_not_deleted_trip(session, trip_uuid)

    if not db_trip:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Trip not found")
    return db_trip


@router.post("", response_model=TripCreate)
def create_trip(trip: TripCreate, session: SessionDep):

    return trips.create_trip(session, trip, user_uuid)


@router.patch("/{trip_uuid}", response_model=TripModify)
def modify_trip(trip: TripModify, session: SessionDep, trip_uuid: str):

    db_trip = trips.get_trip(session, trip_uuid)
    if not db_trip:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Trip not found")

    if db_trip.deleted_at:
        raise HTTPException(
            status.HTTP_406_NOT_ACCEPTABLE, "Cannot modify trip that has been removed"
        )

    return trips.modify_trip(session, trip, trip_uuid)


@router.delete("/{trip_uuid}", response_model=TripBase)
def delete_trip(session: SessionDep, trip_uuid: str):

    db_trip = trips.get_trip(session, trip_uuid)
    if not db_trip:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Trip not found")

    if db_trip.deleted_at:
        raise HTTPException(
            status.HTTP_406_NOT_ACCEPTABLE, "Trip has already been removed"
        )

    return trips.delete_trip(session, trip_uuid, user_uuid)

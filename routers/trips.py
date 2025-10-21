from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, status

import models
from crud import trips
from database import SessionDep
from schemas.trips import TripBase, TripCreate, TripModify

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
    trip_duration_in_days: int | None = None,
    from_start_date: datetime | None = None,
    to_start_date: datetime | None = None,
):
    if from_start_date and to_start_date and from_start_date > to_start_date:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="from_start_date cannot be after to_start_date",
        )

    if limit > 5:
        limit = 5

    return trips.trips_with_filters(
        session,
        from_start_date,
        to_start_date,
        trip_duration_in_days,
        q,
        category,
        limit,
        offset,
    )


@router.get("/{trip_uuid}", response_model=TripBase)
def get_trip(trip_uuid: str, session: SessionDep):

    db_trip = trips.get_trip(session, trip_uuid)

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

    return trips.modify_trip(session, trip, trip_uuid, user_uuid)


@router.delete("/{trip_uuid}", response_model=TripBase)
def delete_trip(session: SessionDep, trip_uuid: str):

    db_trip = trips.get_trip(session, trip_uuid)
    if not db_trip:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Trip not found")

    return trips.delete_trip(session, trip_uuid, user_uuid)

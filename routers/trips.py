import os
from datetime import datetime
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse

from crud import trips
from db import SessionDep
from dependencies.users import get_admin_user
from models import trips as TripsModel
from schemas.trips import (TripBase, TripCreate, TripCreateResponse,
                           TripModify, TripModifyResponse)
from schemas.users import User
from schemas.utils import Status

router = APIRouter(prefix="/trips")
user_uuid = "576590e1-3f56-4a0a-aec5-5d84a319988f"


@router.get("/count")
def get_trips_count(session: SessionDep):
    db_trips = session.query(TripsModel.Trip).count()
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


@router.post("", response_model=TripCreateResponse)
def create_trip(
    trip: TripCreate,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_admin_user)],
):

    return trips.create_trip(session, trip, current_user.user_uuid)


@router.patch("/{trip_uuid}", response_model=TripModifyResponse)
def modify_trip(
    trip: TripModify,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_admin_user)],
    trip_uuid: str,
):

    db_trip = trips.get_trip(session, trip_uuid)
    if not db_trip:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Trip not found")

    return trips.modify_trip(session, trip, trip_uuid, current_user.user_uuid)


@router.delete("/{trip_uuid}", response_model=Status)
def delete_trip(
    session: SessionDep,
    current_user: Annotated[User, Depends(get_admin_user)],
    trip_uuid: str,
):

    db_trip = trips.get_trip(session, trip_uuid)
    if not db_trip:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Trip not found")

    trips.delete_trip(session, trip_uuid, current_user.user_uuid)

    return {"status": "ok"}


@router.get("/{trip_uuid}/background")
def get_background(
    trip_uuid: str,
    session: SessionDep,
):
    db_trip = trips.get_trip(session, trip_uuid)
    if not db_trip:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Trip not found")

    file_extension = db_trip.background_photo
    if not file_extension:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "The background photo does not exists"
        )

    background_path = "./backgrounds"
    file_path = os.path.join(background_path, f"{trip_uuid}.{file_extension}")

    if os.path.exists(file_path):
        return FileResponse(file_path)


@router.delete("/{trip_uuid}/background", response_model=Status)
def delete_background(
    trip_uuid: str,
    _: Annotated[User, Depends(get_admin_user)],
    session: SessionDep,
):
    db_trip = trips.get_trip(session, trip_uuid)
    if not db_trip:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Trip not found")

    file_extension = db_trip.background_photo
    if not file_extension:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "The background photo does not exists"
        )

    background_path = "./backgrounds"
    file_path = os.path.join(background_path, f"{trip_uuid}.{file_extension}")

    if os.path.exists(file_path):
        os.remove(file_path)

    trips.delete_background(session, trip_uuid)

    return {"status": "ok"}

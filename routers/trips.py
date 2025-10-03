from fastapi import APIRouter
from fastapi import HTTPException, status
import models
from schemas import TripBase, TripCreate, TripModify
from crud import trips, participants
from fastapi import HTTPException, status
from database import SessionDep


router = APIRouter(prefix="/trips")


@router.get("/count")
def get_trips_count(session: SessionDep):
    db_trips = session.query(models.Trip).count()
    return db_trips


@router.get("")
def get_trips(session: SessionDep):
    db_trips = session.query(models.Trip).all()
    if not db_trips:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Trips not exist")

    return db_trips


@router.get("/{trip_uuid}", response_model=TripBase)
def get_trip(trip_uuid: str, session: SessionDep):
    db_trip = (
        session.query(models.Trip).filter(models.Trip.trip_uuid == trip_uuid).first()
    )
    if not db_trip:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Trip not found")
    return db_trip


@router.post("", response_model=TripCreate)
def create_trip(trip: TripCreate, session: SessionDep):

    return trips.create_trip(session, trip)


@router.patch("/{trip_uuid}", response_model=TripModify)
def modify_trip(trip: TripModify, session: SessionDep, trip_uuid: str):

    db_trip = trips.get_trip(session, trip_uuid)
    if not db_trip:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Trip not found")

    return trips.modify_trip(session, trip, trip_uuid)


@router.delete("/{trip_uuid}", response_model=TripBase)
def delete_trip(session: SessionDep, trip_uuid: str):

    db_trip = trips.get_trip(session, trip_uuid)
    if not db_trip:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Trip not found")
    
    return trips.delete_trip(session, trip_uuid)
    

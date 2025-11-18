from datetime import date

from sqlmodel import SQLModel


class TripBase(SQLModel):
    name: str
    trip_uuid: str
    category: str
    start_date: date
    end_date: date
    description: str
    payment_schedule: str
    meet_points: list
    background_photo: str | None = None


class TripCreate(SQLModel):
    name: str
    category: str
    start_date: date
    end_date: date
    description: str
    payment_schedule: str
    meet_points: list
    background_photo: str


class TripCreateResponse(TripCreate):
    trip_uuid: str


class TripModify(SQLModel):
    name: str | None = None
    category: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    description: str | None = None
    payment_schedule: str | None = None
    meet_points: list | None = None
    background_photo: str | None = None


class TripModifyResponse(TripModify):
    trip_uuid: str

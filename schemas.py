from datetime import date, datetime

from sqlmodel import SQLModel


class TripBase(SQLModel):
    name: str
    category: str
    start_date: date
    end_date: date
    description: str
    payment_schedule: str
    meet_points: list
    background_photo: str


class TripCreate(SQLModel):
    name: str
    category: str
    start_date: date
    end_date: date
    description: str
    payment_schedule: str
    meet_points: list
    background_photo: str


class TripModify(SQLModel):
    name: str | None = None
    category: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    description: str | None = None
    payment_schedule: str | None = None
    meet_points: list | None = None
    background_photo: str | None = None


class ParticipantBase(SQLModel):
    name: str
    surname: str
    email: str
    phone: str
    gender: str
    birth_date: datetime
    chosen_meet_point: str | None
    group_code: str | None
    comments: str | None


class ParticipantCreate(SQLModel):
    name: str
    surname: str
    email: str
    phone: str
    gender: str
    birth_date: datetime
    trip_uuid: str
    chosen_meet_point: str | None = None
    group_code: str | None = None
    comments: str | None = None


class ParticipantModify(SQLModel):
    name: str | None = None
    surname: str | None = None
    email: str | None = None
    phone: str | None = None
    gender: str | None = None
    birth_date: datetime | None = None
    chosen_meet_point: str | None = None
    group_code: str | None = None
    comments: str | None = None

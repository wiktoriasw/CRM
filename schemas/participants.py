from datetime import datetime

from sqlmodel import SQLModel


class ParticipantBase(SQLModel):
    name: str
    participant_uuid: str
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


class ParticipantCreateResponse(ParticipantCreate):
    participant_uuid: str


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


class ParticipantModifyResponse(ParticipantModify):
    participant_uuid: str

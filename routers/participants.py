from typing import List, Annotated
from fastapi import APIRouter, HTTPException, status, Depends

import models
from crud import participants, users
from database import SessionDep
from schemas.participants import (ParticipantBase, ParticipantCreate,
                                  ParticipantModify)
from schemas.users import User
from sqlalchemy.exc import DataError

router = APIRouter(prefix="/participants")
user_uuid = "576590e1-3f56-4a0a-aec5-5d84a319988f"


def parse_participant(participant: models.Participant) -> models.Participant:
    return {
        **participant.__dict__,
        "gender": participant.gender.name,
    }


@router.get("/", response_model=List[ParticipantBase])
def get_partcipants(
    session: SessionDep,
    q: str | None = None,
    gender: str | None = None,
    meet_point: str | None = None,
    limit: int = 3,
    offset: int = 0,
):
    if limit > 5:
        limit = 5

    if gender:
        gender = gender.lower()

        if gender not in models.UserGender.__members__:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Given gender not found"
            )

    if meet_point:
        meet_point = meet_point.lower()    

    return map(
        parse_participant,
        participants.participants_with_filters(
            session, q, limit, offset, gender, meet_point
        ),
    )


@router.get("/{participant_uuid}", response_model=ParticipantBase)
def get_participant(session: SessionDep, participant_uuid: str):
    db_participant = participants.get_participant(session, participant_uuid)

    if not db_participant:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Participant not found")

    return parse_participant(db_participant)


@router.post("/", response_model=ParticipantCreate)
def create_participant(
    participant: ParticipantCreate,
    current_user: Annotated[User, Depends(users.get_current_user)],
    session: SessionDep):

    try:
        return parse_participant(
        participants.create_participant(session, participant, current_user.user_uuid)
    )
    except DataError:
        raise(HTTPException(status.HTTP_406_NOT_ACCEPTABLE, 'Use lowercase for the gender'))


@router.patch("/{participant_uuid}", response_model=ParticipantModify)
def modify_participant(
    participant: ParticipantModify,
    current_user: Annotated[User, Depends(users.get_current_user)],
    session: SessionDep,
    participant_uuid: str
):

    db_participant = participants.get_participant(session, participant_uuid)

    if not db_participant:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Participant not exists")

    return participants.modify_participant(
        session, participant, participant_uuid, current_user.user_uuid
    )


@router.delete("/{participant_uuid}", response_model=ParticipantBase)
def delete_participant(
    current_user: Annotated[User, Depends(users.get_current_user)],
    session: SessionDep,
    participant_uuid: str):

    db_participant = participants.get_participant(session, participant_uuid)
    if not db_participant:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Participant not found")

    return parse_participant(
        participants.delete_participant(session, participant_uuid, current_user.user_uuid)
    )

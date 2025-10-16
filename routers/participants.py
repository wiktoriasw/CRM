from typing import List

from fastapi import APIRouter, HTTPException, status

from crud import participants
from database import SessionDep
from schemas.participants import ParticipantBase, ParticipantCreate, ParticipantModify

router = APIRouter(prefix="/participants")
user_uuid = "576590e1-3f56-4a0a-aec5-5d84a319988f"


@router.get("/", response_model=List[ParticipantBase])
def get_partcipants(
    session: SessionDep, q: str | None = None, limit: int = 3, offset: int = 0
):
    if limit > 5:
        limit = 5

    return participants.participants_with_filters(session, q, limit, offset)


@router.get("/{participant_uuid}", response_model=ParticipantBase)
def get_participant(session: SessionDep, participant_uuid: str):
    db_participant = participants.get_participant(session, participant_uuid)

    if not db_participant:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Participant not found")

    return db_participant


@router.post("/", response_model=ParticipantCreate)
def create_participant(participant: ParticipantCreate, session: SessionDep):

    return participants.create_participant(session, participant, user_uuid)


@router.patch("/{participant_uuid}", response_model=ParticipantModify)
def modify_participant(
    participant: ParticipantModify, session: SessionDep, participant_uuid: str
):

    db_participant = participants.get_participant(session, participant_uuid)

    if not db_participant:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Participant not exists")

    return participants.modify_participant(
        session, participant, participant_uuid, user_uuid
    )


@router.delete("/{participant_uuid}", response_model=ParticipantBase)
def delete_participant(session: SessionDep, participant_uuid: str):

    db_participant = participants.get_participant(session, participant_uuid)
    if not db_participant:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Participant not found")

    return participants.delete_participant(session, participant_uuid, user_uuid)

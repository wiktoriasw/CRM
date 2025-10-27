from sqlalchemy import func
from sqlalchemy.orm import Session

from models import participants
from schemas.participants import ParticipantCreate, ParticipantModify


def _get_not_deleted_participants(db: Session):
    return db.query(participants.Participant).filter(
        participants.Participant.deleted_at == None
    )


def get_participant(db: Session, participant_uuid: str):
    return (
        _get_not_deleted_participants(db)
        .filter(participants.Participant.participant_uuid == participant_uuid)
        .first()
    )


def participants_with_filters(
    db: Session,
    q: str | None = None,
    limit: int = 3,
    offset: int = 0,
    gender: str | None = None,
    meet_point: str | None = None,
):
    query = _get_not_deleted_participants(db)

    if q:
        query = query.filter(
            (participants.Participant.name.ilike("%" + q + "%"))
            | (participants.Participant.surname.ilike("%" + q + "%"))
        )
    if gender:
        query = query.filter(participants.Participant.gender == gender)

    if meet_point == "NULL":
        query = query.filter(
            participants.Participant.chosen_meet_point == None
        )
    elif meet_point:
        query = query.filter(
            func.lower(participants.Participant.chosen_meet_point) == meet_point
        )

    query = query.limit(limit).offset(offset)

    db_participants = query.all()

    return db_participants


def create_participant(db: Session, participant: ParticipantCreate, user_uuid: str):
    db_participant = participants.Participant(**participant.model_dump())
    db_participant.user_uuid = user_uuid
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)

    return db_participant


def modify_participant(
    db: Session,
    participant_modify: ParticipantModify,
    participant_uuid: str,
    user_uuid: str,
):
    db_participant = get_participant(db, participant_uuid)
    db_participant.user_uuid = user_uuid

    update_data = {
        k: v
        for k, v in participant_modify.model_dump(exclude_unset=True).items()
        if v is not None
    }

    if update_data:
        for key, value in update_data.items():
            setattr(db_participant, key, value)

        db_participant.updated_by = user_uuid
        db.commit()

    return db_participant


def delete_participant(db: Session, participant_uuid: str, user_uuid: str):
    db_participant = get_participant(db, participant_uuid)
    db_participant.user_uuid = user_uuid
    db_participant.deleted_at = func.now()
    db.commit()
    db.refresh(db_participant)

    return db_participant

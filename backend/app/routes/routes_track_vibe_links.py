from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import Session, SQLModel, select

from app.db.session import get_session
from app.models.links import TrackVibeLink

router = APIRouter(prefix="/track_vibe_links", tags=["track_vibe_links"])


class TrackVibeLinkCreate(SQLModel):
    track_id: int
    vibe_id: int


class TrackVibeLinkUpdate(SQLModel):
    track_id: Optional[int] = None
    vibe_id: Optional[int] = None


def _rollback_and_raise(
    session: Session,
    status_code: int,
    detail: str,
) -> None:
    session.rollback()
    raise HTTPException(status_code=status_code, detail=detail)


def _get_record(session: Session, track_id: int, vibe_id: int):
    return session.exec(
        select(TrackVibeLink).where(
            TrackVibeLink.track_id == track_id,
            TrackVibeLink.vibe_id == vibe_id,
        )
    ).first()


@router.get("", response_model=list[TrackVibeLink])
def list_track_vibe_links(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    session: Session = Depends(get_session),
):
    try:
        return session.exec(select(TrackVibeLink).offset(offset).limit(limit)).all()
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.post("", response_model=TrackVibeLink, status_code=201)
def create_track_vibe_link(
    payload: TrackVibeLinkCreate,
    session: Session = Depends(get_session),
):
    try:
        record = TrackVibeLink.model_validate(payload)
        session.add(record)
        session.commit()
        session.refresh(record)
        return record
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.get("/{track_id}/{vibe_id}", response_model=TrackVibeLink)
def get_track_vibe_link(
    track_id: int,
    vibe_id: int,
    session: Session = Depends(get_session),
):
    try:
        record = _get_record(session, track_id, vibe_id)
        if not record:
            raise HTTPException(
                status_code=404,
                detail="TrackVibeLink not found",
            )
        return record
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.patch("/{track_id}/{vibe_id}", response_model=TrackVibeLink)
def update_track_vibe_link(
    track_id: int,
    vibe_id: int,
    payload: TrackVibeLinkUpdate,
    session: Session = Depends(get_session),
):
    try:
        record = _get_record(session, track_id, vibe_id)
        if not record:
            raise HTTPException(
                status_code=404,
                detail="TrackVibeLink not found",
            )
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(record, key, value)
        session.add(record)
        session.commit()
        session.refresh(record)
        return record
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.delete("/{track_id}/{vibe_id}", status_code=204)
def delete_track_vibe_link(
    track_id: int,
    vibe_id: int,
    session: Session = Depends(get_session),
):
    try:
        record = _get_record(session, track_id, vibe_id)
        if not record:
            raise HTTPException(
                status_code=404,
                detail="TrackVibeLink not found",
            )
        session.delete(record)
        session.commit()
        return None
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))

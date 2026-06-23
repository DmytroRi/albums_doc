from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import Field, Session, SQLModel, select

from app.db.session import get_session
from app.models.tracks import Track, TrackRead, TrackUpdate

router = APIRouter(prefix="/tracks", tags=["tracks"])


class TrackCreate(SQLModel):
    title: str
    length_seconds: Optional[int] = None
    track_order: int
    album_id: int = Field(foreign_key="albums.id")


class TrackPatch(TrackUpdate):
    album_id: Optional[int] = Field(default=None, foreign_key="albums.id")


class TrackReadWithAlbum(TrackRead):
    album_id: int


def _rollback_and_raise(
    session: Session,
    status_code: int,
    detail: str,
) -> None:
    session.rollback()
    raise HTTPException(status_code=status_code, detail=detail)


@router.get("", response_model=list[TrackReadWithAlbum])
def list_tracks(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    session: Session = Depends(get_session),
):
    try:
        return session.exec(select(Track).offset(offset).limit(limit)).all()
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.post("", response_model=TrackReadWithAlbum, status_code=201)
def create_track(
    payload: TrackCreate,
    session: Session = Depends(get_session),
):
    try:
        record = Track.model_validate(payload)
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


@router.get("/{record_id}", response_model=TrackReadWithAlbum)
def get_track(
    record_id: int,
    session: Session = Depends(get_session),
):
    try:
        record = session.get(Track, record_id)
        if not record:
            raise HTTPException(
                status_code=404,
                detail="Track not found",
            )
        return record
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.patch("/{record_id}", response_model=TrackReadWithAlbum)
def update_track(
    record_id: int,
    payload: TrackPatch,
    session: Session = Depends(get_session),
):
    try:
        record = session.get(Track, record_id)
        if not record:
            raise HTTPException(
                status_code=404,
                detail="Track not found",
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


@router.delete("/{record_id}", status_code=204)
def delete_track(
    record_id: int,
    session: Session = Depends(get_session),
):
    try:
        record = session.get(Track, record_id)
        if not record:
            raise HTTPException(
                status_code=404,
                detail="Track not found",
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
